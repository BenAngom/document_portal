import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    
    def __init__(self,base_dir:str="/Users/benudhorangom/Documents/document_portal/data/document_compare"):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def delete_existing_files(self):
        """
        delete all existing files in the specific paths
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File deleted ",path=str(file))
                self.log.info("Directory cleaned ", directory=str(self.base_dir))
        except Exception as e:
            self.log.error("Error deleting existing files", error=str(e))
            raise DocumentPortalException("An Error occurred while deleting existing files", sys)
    
    def save_uploaded_file(self, reference_file, actual_file):
        """save the uploaded file to a specific directory
        """
        try:
            self.delete_existing_files()
            self.log.info("Deleted existing files in the upload directory")
            
            ref_path=self.base_dir / reference_file.name
            act_path=self.base_dir / actual_file.name
            
            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed.")
            
            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer())
                
            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer())
                
            self.log.info("Successfully saved uploaded files", reference_file=str(ref_path), actual_file=str(act_path))
            return ref_path, act_path
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
            

    def combine_documents(self)-->str:
        try:
            content_dict = {}
            doc_parts = []
            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix.lower() == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)
                    
            for filename, content in content_dict.items():
                doc_parts.append(f"Document Name: {filename}\n{Content}")
                
            combined_text = "\n\n".join(doc_parts)
            self.log.info("Successfully combined documents", document_count=len(doc_parts))
            return combined_text
            
        except Exception as e:
            self.log.error("Error combining documents", error=str(e))
            
            raise DocumentPortalException("An Error occurred while combining the documents", sys)
            
        