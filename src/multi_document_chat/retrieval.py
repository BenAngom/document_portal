import sys
import os
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS

from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from prompt.prompt_library import prompt_library
from model.models import PromptType

class ConversationalRAG:
    def __init__(self, session_id:sys, retriever=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.llm=self._load_llm()
            self.contextualize_prompt:CharPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt:ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            if retriever is None:
                raise ValueError("Retriever cannot be none")
            self.retriever=retriever
            self._build_lcel_chain()
            self.log.info("ConversationalRAG initialized", session_id=self.session_id)
            
        except Exception as e:
            self.log.error("Failed to initialize conversationalRAG", error=str(e))
            raise DocumentPortalException("Initialization error in ConversationRAG ",sys)
        
        
    def load_retriever_from_faiss(self, index_path: str):
        # Logic to load a retriever from a FAISS index
        """Load a FAISS vectorstore from disk and convert to retriever
        """
        
        try:
            embeddings = ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found: {index_path}")
            vectorstore = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True,
            )
            
            self.retriever = vectorstore.as_retriever(search_type="similarity", session_kwargs={"k":5})  
            self.log.info("FAISS retriever loaded successfully", index_path=index_path, session_id=self.session_id)
            
            self._build_lcel_chain()
            return self.retriever
            
        except Exception as e:
            self.log.error("Failed to load retriver from FAISS", error=str(e))
            raise DocumentPortalException("Loading error in ConversationRAG", sys)
    
    def invoke(self):
        # Logic to handle the conversational retrieval process
        try:
            pass
        except Exception as e :
            self.log.error("Failed to invoke ConversationalRAG",error=str(e))
            raise DocumentPortalException("Invocation error in ConversationRAG" sys)
    
    def _load_llm(self):
        # Logic to load the language model for generating responses
        try:
            llm = ModelLoader().load_llm()
            if not llm:
                raise ValueError("LLM could not be loaded")
            self.log.info("LLM Loaded successfully", session_id=self._session_id)
            return llm
        except Exception as e :
            self.log.error("Failed to load LLM",error=str(e))
            raise DocumentPortalException("LLM loading error in ConversationRAG" sys)
    
    
    @staticmethod
    def _format_docs(docs) -> str:
        return "\n\n".join(getattr(d, "page_content", str(d)) for d in docs)

    def _build_lcel_chain(self):
        try:
            if self.retriever is None:
                raise DocumentPortalException("No retriever set before building chain", sys)

            # 1) Rewrite user question with chat history context
            question_rewriter = (
                {"input": itemgetter("input"), "chat_history": itemgetter("chat_history")}
                | self.contextualize_prompt
                | self.llm
                | StrOutputParser()
            )

            # 2) Retrieve docs for rewritten question
            retrieve_docs = question_rewriter | self.retriever | self._format_docs

            # 3) Answer using retrieved context + original input + chat history
            self.chain = (
                {
                    "context": retrieve_docs,
                    "input": itemgetter("input"),
                    "chat_history": itemgetter("chat_history"),
                }
                | self.qa_prompt
                | self.llm
                | StrOutputParser()
            )

            log.info("LCEL graph built successfully", session_id=self.session_id)
        except Exception as e:
            log.error("Failed to build LCEL chain", error=str(e), session_id=self.session_id)
            raise DocumentPortalException("Failed to build LCEL chain", sys)