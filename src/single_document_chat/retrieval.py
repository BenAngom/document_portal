import sys
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_messages_histories import ChatMessagesHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import Modelloader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType 

class ConversationalRAG:
    
    def __init__(self , session_id: str, retriever) -> None:
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.loader = Modelloader()
            self.vector_store = FAISS()
            self.chat_history = ChatMessagesHistory()
            
        except Exception as e:
            self.log.error("Error initializing ConversationalRAG", error=str(e))
            raise DocumentPortalException("An Error occurred while initializing ConversationalRAG", sys)
        
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error loading LLM", error=str(e))
            raise DocumentPortalException("An Error occurred while loading the LLM", sys)
        
    def _getSessionHistory(self, session_id: str):
        try:
            pass
        except Exception as e:
            self.log.error("Error getting session history", session_id=session_id, error=str(e))
            raise DocumentPortalException("An Error occurred while getting the session history", sys)
        
    def load_retriever_from_FAISS(self, session_id: str):
        try:
            pass
        except Exception as e:
            self.log.error("Error loading retriever from FAISS", session_id=session_id, error=str(e))
            raise DocumentPortalException("An Error occurred while loading the retriever from FAISS", sys)
        
    def invoke(self, query: str, session_id: str):
        try:
            pass
        except Exception as e:
            self.log.error("Error invoking ConversationalRAG", session_id=session_id, query=query, error=str(e))
            raise DocumentPortalException("An Error occurred while invoking ConversationalRAG", sys)