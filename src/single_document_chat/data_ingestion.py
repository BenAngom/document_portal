import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class SingleDocIngestion:
    
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.loader = Modelloader()
            self.pdf_loader = PyPDFLoader()
            self.text_splitter = RecursiveCharacterTextSplitter()
            self.vector_store = FAISS()
            
        except Exception as e:
            self.log.error("Error initializing SingleDocIngestion", error=str(e))
            raise DocumentPortalException("An Error occurred while initializing SingleDocIngestion", sys)
        
        
    def ingest_files(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error ingesting files", error=str(e))
            raise DocumentPortalException("An Error occurred while ingesting files", sys)
        
    def _create_retriever(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error creating retriever", error=str(e))
            raise DocumentPortalException("An Error occurred while creating the retriever", sys)