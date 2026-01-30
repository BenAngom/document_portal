import os
import fitz # PyMuPDF
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """
    Handles PDF saving and reading operations.
    Automatically logs all actions and supports session-based organization
    """
    
    def __init__(self,data_dir=None,session_id=None):
        try:
            self.log=CustomLogger().get_logger(__name__) # name of the current module
            
            self.data_dir=data_dir or os.getenv(
            "DATA_STORAGE_PATH",
            os.path.join(os.getcwd(),"data","document_analysis")
            )
            self.session_id=session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        
            #create base session directory if not exists
            self.session_path=os.path.join(self.data_dir,self.session_id)
            os.makedirs(self.session_path,exist_ok=True)
            self.log.info("DocumentHandler initialized with session ID",session_id= self.session_id, session_path=self.session_path)
            
        except Exception as e:
            self.log.error("Error initializing DocumentHandler", error=str(e))
            raise DocumentPortalException("Error initializing DocumentHandler",e) from e

    def save_pdf(self, uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)
            
            if not filename.lower().endswith(".pdf"):
                raise DocumentPortalException("Invalid file type. Only PDFs are allowed.")
            
            save_path = os.path.join(self.session_path, filename)
            
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            self.log.info("PDF saved successfully", file=filename, save_path=save_path, session_id=self.session_id)
            return save_path
        except Exception as e:
            self.log.error("Failed to save PDF", error=str(e), session_id=self.session_id)
            raise DocumentPortalException("Failed to save PDF: ", e) from e

    def read_pdf(self, pdf_path:str) -> str:
        try:
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc,start=1):
                    text_chunks.append(f"\n --- Page {page_num} --- \n{page.get_text()}")
            text = "\n".join(text_chunks)
            
            self.log.info("PDF read successfully", pdf_path=pdf_path, session_id=self.session_id,pages=len(text_chunks))
            return text
            
        except Exception as e:
            self.log.error("Error reading PDF: {e}")
            raise DocumentPortalException("Error reading PDF", e) from e
    
    
# for testing this class
if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    handler = DocumentHandler()
    
    pdf_path = r"/Users/benudhorangom/Documents/document_portal/data/document_analysis/NIPS-2017-attention-is-all-you-need-Paper.pdf" # Ensure this file exists for testing
    
    class DummyFile:
        def __init__(self, file_path):
            self.name = Path(file_path).name
            self._file_path = file_path
        def getbuffer(self):
            return open(self._file_path, "rb").read()
        
    dummy_pdf = DummyFile(pdf_path)
    
    handler = DocumentHandler(session_id="test_session_001")
    
    try:
        saved_path = handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {saved_path}")  
        
        content = handler.read_pdf(saved_path)
        print("PDF content read successfully.")
        print(content[:500])  # Print first 500 characters of the PDF content
        
    except DocumentPortalException as e:
        print(f"An error occurred: {e}")
        
        
    
    