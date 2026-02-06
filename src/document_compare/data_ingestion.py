import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    
    def __init__(self,base_dir):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def delete_existing_files(self):
        """
        delete all existing files in the specific paths
        """
        try:
            pass
        except Exception as e:
            self.log.error("Error deleting existing files", error=str(e))
            raise DocumentPortalException("An Error occurred while deleting existing files", sys)
    
    def save_uploaded_file(self):
        """save the uploaded file to a specific directory
        """
        try:
            pass
        except Exception as e:
            self.log.error("Error saving uploaded file", error=str(e))
            raise DocumentPortalException("An Error occurred while saving the uploaded file", sys)
        
    
    def read_pdf(self,pdf_path: Path) -> str:
        """
        read the file from a specific location

        """
        try:
            with fitz.open(self, pdf_path:str) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"The PDF document is encrypted and cannot be processed.{pdf_path.name}")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    
                    if(text.strip()):
                        all_text.append(f"\n Page {page_num + 1} --- \n{text}")
                self.log.info(f"Successfully read PDF: ", file=str(pdf_path), pages=len(all_text)
                return "\n".join(all_text)
        except Exception as e:
            self.log.error("Error reading PDF", error=str(e))
            raise DocumentPortalException("An Error occurred while reading the PDF", sys)