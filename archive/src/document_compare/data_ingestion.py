import sys
from pathlib import Path
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    
    def __init__(self,base_dir: str="/Users/benudhorangom/Documents/document_portal/data/document_compare", session_id=None):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id=session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        self.log.info("DocumentIngestion initialized", session_path=str(self.session_path))
    
    # def delete_existing_files(self):
    #     """
    #     delete all existing files in the specific paths
    #     """
    #     try:
    #         if self.base_dir.exists() and self.base_dir.is_dir():
    #             for file in self.base_dir.iterdir():
    #                 if file.is_file():
    #                     file.unlink()
    #                     self.log.info("File deleted ",path=str(file))
    #             self.log.info("Directory cleaned ", directory=str(self.base_dir))
    #     except Exception as e:
    #         self.log.error("Error deleting existing files", error=str(e))
    #         raise DocumentPortalException("An Error occurred while deleting existing files", sys)
    
    def save_uploaded_files(self, reference_file, actual_file):
        """save the uploaded file to a specific directory
        """
        try:
            ref_path = self.session_path / reference_file.name
            act_path = self.session_path / actual_file.name
            
            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed.")
            
            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer())
                
            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer())
                
            self.log.info("Successfully saved uploaded files", reference=str(ref_path), actual=str(act_path), session=self.session_id)
            return ref_path, act_path
        except Exception as e:
            self.log.error("Error saving uploaded file", error=str(e), session=self.session_id)
            raise DocumentPortalException("An Error occurred while saving the uploaded file", sys)
        
    
    def read_pdf(self,pdf_path: Path)->str:
        """
        reads a pdf file and extracts text from each page
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"The PDF document is encrypted and cannot be processed.{pdf_path.name}")
                
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    
                    if(text.strip()):
                        all_text.append(f"\n Page {page_num + 1} --- \n{text}")
                        
                self.log.info(f"Successfully read PDF: ", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text)
        except Exception as e:
            self.log.error("Error reading PDF", file=str(pdf_path), error=str(e))
            raise DocumentPortalException("An Error occurred while reading the PDF", sys)
            

    def combine_documents(self)->str:
        try:
            doc_parts = []
            for file in sorted(self.session_path.iterdir()):
                if file.is_file() and file.suffix.lower() == ".pdf":
                    content = self.read_pdf(file)
                    
                    print(file.name, "content length:", len(content))
                    doc_parts.append(f"Document : {file.name}\n{content}")
                
            combined_text = "\n\n".join(doc_parts)
            self.log.info("Successfully combined documents", count=len(doc_parts), session=self.session_id)
            
            print("SESSION PATH:", self.session_path)
            print("FILES:", list(self.session_path.iterdir()))
            return combined_text
    
        except Exception as e:
            self.log.error("Error combining documents", error=str(e), session=self.session_id)  
            raise DocumentPortalException("An Error occurred while combining the documents", sys)
            
        
        
    def clean_old_sessions(self, keep_latest: int = 3):
        try:
            sessions = sorted([f for f in self.base_dir.iterdir() if f.is_dir()], reverse=True)
            for folder in sessions[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()
                self.log.info("Old session folder deleted", path=str(folder))
        except Exception as e:
            self.log.error("Error cleaning old sessions", error=str(e))
            raise DocumentPortalException("Error cleaning old sessions", sys) 