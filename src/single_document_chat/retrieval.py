import sys
import os
from urllib import response
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
#from langchain_community.chat_messages_histories import ChatMessagesHistory
from langchain.memory import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType 

class ConversationalRAG:
    
    def __init__(self , session_id: str, retriever) -> None:
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.retriever = retriever
            self.llm = self._load_llm()
            self.store = {}
            self.contextualize_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.answer_prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            
            ##self.history_aware_retriever = create_history_aware_retriever(self.llm, self.retriever, self.contextualize_prompt)
            ##self.log.info("ConversationalRAG initialized, Created history aware retriever", session_id=session_id)
            
            self.history_aware_retriever = self.retriever
            self.log.info("ConversationalRAG initialized", session_id=session_id)
            
            self.qa_chain = create_stuff_documents_chain(self.llm, self.answer_prompt)
            ##self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.qa_chain)
            
            def safe_query(x):
                if isinstance(x, dict):
                    query = x.get("input", "")
                else:
                    query = x

                if not isinstance(query, str):
                    query = str(query)

                return query
            
            def safe_history(x):
                if isinstance(x, dict):
                    return x.get("chat_history", [])
                return []
            
            self.rag_chain = (
                {
                    "context": lambda x: self.retriever.invoke(safe_query(x)),
                    "input": safe_query,
                    "chat_history": safe_history,
                }
                | self.qa_chain
            )
            
            
            self.log.info("Created RAG chain", session_id=session_id)
            
            self.chain = RunnableWithMessageHistory(
                self.rag_chain, 
                self._getSessionHistory,
                input_message_key="input",
                output_message_key="answer",
                history_message_key="chat_history"
                )
            self.log.info("Wrapped RAG chain with message history", session_id=session_id)
        except Exception as e:
            self.log.error("Error initializing ConversationalRAG", error=str(e))
            raise DocumentPortalException("An Error occurred while initializing ConversationalRAG", sys)
        
    def _load_llm(self):
        try:
            llm = ModelLoader().load_llm()
            self.log.info("LLM loaded successfully")
            return llm
        except Exception as e:
            self.log.error("Error loading LLM", error=str(e))
            raise DocumentPortalException("An Error occurred while loading the LLM", sys)
        
    def _getSessionHistory(self, session_id: str):
        try:
            if session_id not in self.store:
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]
        except Exception as e:
            self.log.error("Error getting session history", session_id=session_id, error=str(e))
            raise DocumentPortalException("An Error occurred while getting the session history", sys)
        
    def load_retriever_from_FAISS(self, index_path :str, session_id: str):
        try:
            embeddings = ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found at {index_path}")
            
            vectorstore = FAISS.load_local(index_path, embeddings)
            self.log.info("Loaded retriever from FAISS index", index_path=index_path)
            return vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})
        except Exception as e:
            self.log.error("Error loading retriever from FAISS", session_id=session_id, error=str(e))
            raise DocumentPortalException("An Error occurred while loading the retriever from FAISS", sys)
    
        
    # def invoke(self, user_input: str)->str:
    #     try:
    #         self.chain.invoke(
    #             {"input": user_input},
    #             config = {"configurable": {"session_id": self.session_id}}
    #         )
    #         answer = response.get("answer", "No Answer")
    #         if not answer:
    #             self.log.warning("Empty answer received", session_id=self.session_id)
    #         self.log.info("ConversationalRAG invoked successfully", session_id=self.session_id, user_input=user_input, answer_preview=answer[:150])
    #         return answer
    #     except Exception as e:
    #         self.log.error("Error invoking ConversationalRAG", session_id=self.session_id, user_input=user_input, error=str(e))
    #         raise DocumentPortalException("An Error occurred while invoking ConversationalRAG", sys)
    
    def invoke(self, user_input: str) -> str:
        try:
            response = self.chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": self.session_id}}
            )   

            ##answer = response.get("answer", "No Answer")
            
            if isinstance(response, dict):
                answer = response.get("answer", "No Answer")
            else:
                answer = response

            if not answer:self.log.warning("Empty answer received",session_id=self.session_id)
            self.log.info("ConversationalRAG invoked successfully",session_id=self.session_id,user_input=user_input,answer_preview=answer[:150],)

            return answer

        except Exception as e:
            self.log.error("Error invoking ConversationalRAG",session_id=self.session_id,user_input=user_input,error=str(e),)
            raise DocumentPortalException("An Error occurred while invoking ConversationalRAG",sys,)
