import uuid
from pathlib import Path
import sys
from datetime import datetime,timezone
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader



class DocumentIngestor:
    
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt",".md"}
    def __init__(self, temp_dir:str = "/Users/benudhorangom/Documents/document_portal/data/multi_doc_chat", faiss_dir: str = "faiss_index",session_id: str | None = None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            
            #base dirs
            self.temp_dir = Path(temp_dir)
            self.faiss_dir = Path(faiss_dir)
            temp_dir.mkdir(parents=True,exist_ok=True)
            faiss_dir.mkdir(parents=True,exist_ok=True)
            
            #sessionized paths
            self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True,exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True,exist_ok=True)
            
            self.model_loader = ModelLoader()
            self.log.info("DocumentIngestor Initialized ",
                temp_base=str(self.temp_dir), 
                faiss_base=str(self.faiss_dir),
                session_id=self.session_id,
                temp_path=str(self.session_temp_dir),
                faiss_path=str(self.session_faiss_dir),
            )
            
        except Exception as e:
            self.log.error("Failed to initialized DocumentIngestor", error=str(e))
            raise DocumentPortalException("Initialization Error in DocumentIngestor" , sys)
        
        

    def ingest_files(self):
        # Logic to ingest documents from the specified source
        try:
            pass
        except Exception as e:
            self.log.error("Failed to ingest files", error=str(e))
            raise DocumentPortalException("Ingestion error in DocumentIngestor", sys)
    
    def _create_retriever(self, document):
        # Logic to create a retriever for the ingested documents
        try:
            pass
        except Exception as e:
            self.log.error("", error=str(e))
            raise DocumentPortalException("", sys)