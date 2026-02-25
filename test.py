# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.data_analysis import DocumentAnalyzer

# # Path to the PDF file you want to test
# pdf_file_path = r"/Users/benudhorangom/Documents/document_portal/data/document_analysis/Open Foundation and Fine-Tuned Chat Models.pdf"

# # Dummy file wrapper to simulate uploaded file (Streamlit nstyle)
# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path
#     def getbuffer(self):
#         return open(self._file_path, "rb").read()
    
# def main():
#     try:
#         # --------------STEP 1: DATA INGESTION----------------
#         print("Starting PDF data ingestion...")
#         dummy_pdf = DummyFile(pdf_file_path)
        
#         pdf_handler = DocumentHandler(session_id="test_ingestion_analysis")
            
#         saved_pdf_path = pdf_handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_pdf_path}")
            
#         pdf_content = pdf_handler.read_pdf(saved_pdf_path)
#         print("PDF content read successfully.")
#         print(pdf_content[:500])  # Print first 500 characters of the PDF content
            
#         # --------------STEP 2: DATA ANALYSIS----------------
#         print("Starting document analysis...")
#         analyzer = DocumentAnalyzer() # Load LLM + Parser
#         analysis_results = analyzer.analyze_document(pdf_content)
            
#         #--------------STEP 3: OUTPUT RESULTS----------------
#         print("Document analysis completed. Results:")
#         for key, value in analysis_results.items():
#             print(f"{key}: {value}")
                
#     except Exception as e:
#         print(f"An error occurred during testing: {e}")
            
            
# if __name__ == "__main__":
#     main()  



# Testing code for document comparison using LLMs
import io
from pathlib import Path
from src.document_compare.data_ingestion import DocumentIngestion
from src.document_compare.document_comparator import DocumentComparatorLLM

# ---- Setup: Load local PDF files as if they were "uploaded" ---- #
def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())  # simulate .getbuffer()

# ---- Step 1: Save and combine PDFs ---- #
def test_compare_documents():
    ref_path = Path("/Users/benudhorangom/Documents/document_portal/data/document_compare/Long_Report_V1.pdf")
    act_path = Path("/Users/benudhorangom/Documents/document_portal/data/document_compare/Long_Report_V2.pdf")


    # Wrap them like Streamlit UploadedFile-style
    class FakeUpload:
        def __init__(self, file_path: Path):
            self.name = file_path.name
            self._buffer = file_path.read_bytes()

        def getbuffer(self):
            return self._buffer

    # Instantiate
    comparator = DocumentIngestion()
    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    # Save files and combine
    ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text = comparator.combine_documents()
    comparator.clean_old_sessions(keep_latest=3)

    print("\n Combined Text Preview (First 1000 chars):\n")
    print(combined_text[:1000])

    # ---- Step 2: Run LLM comparison ---- #
    llm_comparator = DocumentComparatorLLM()
    comparison_df = llm_comparator.compare_documents(combined_text)
    
    print("\n ===COMPARISON RESULT:\n")
    print(comparison_df.head())  # Print first few rows of the comparison DataFrame

if __name__ == "__main__":
    test_compare_documents()

# # Testing code for document chat functionality

# import sys
# from pathlib import Path
# from langchain_community.vectorstores import FAISS
# from src.single_document_chat.data_ingestion import SingleDocIngestor
# from src.single_document_chat.retrieval import ConversationalRAG
# from utils.model_loader import ModelLoader

# FAISS_INDEX_PATH = Path("faiss_index")

# def test_conversational_rag_on_pdf(pdf_path:str, question:str):
#     try:
#         model_loader = ModelLoader()
        
#         index_file = FAISS_INDEX_PATH / "index.faiss"

        
#         if index_file.exists():
#             print("Loading existing FAISS index...")
#             embeddings = model_loader.load_embeddings()
#             vectorstore = FAISS.load_local(folder_path=str(FAISS_INDEX_PATH), embeddings=embeddings,allow_dangerous_deserialization=True)
#             retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#         else:
#             # Step 2: Ingest document and create retriever
#             print("FAISS index not found. Ingesting PDF and creating index...")
#             with open(pdf_path, "rb") as f:
#                 uploaded_files = [f]
#                 #session_id = "test_conversational_rag"
#                 ingestor = SingleDocIngestor()
#                 retriever = ingestor.ingest_files(uploaded_files)
                
#         print("Running Conversational RAG...")
#         session_id = "test_conversational_rag"
#         rag = ConversationalRAG(retriever=retriever, session_id=session_id)
#         response = rag.invoke(question)
#         print(f"\nQuestion: {question}\nAnswer: {response}")
                    
#     except Exception as e:
#         print(f"Test failed: {str(e)}")
#         sys.exit(1)
    
# if __name__ == "__main__":
#     # Example PDF path and question
#     pdf_path = "/Users/benudhorangom/Documents/document_portal/data/single_document_chat/NIPS-2017-attention-is-all-you-need-Paper.pdf"
#     question = "What is the significance of the attention mechanism? can you explain it in simple terms?"

#     if not Path(pdf_path).exists():
#         print(f"PDF file does not exist at: {pdf_path}")
#         sys.exit(1)
    
#     # Run the test
#     test_conversational_rag_on_pdf(pdf_path, question)




# ## testing for multidoc chat
# import sys
# from pathlib import Path
# from src.multi_document_chat.data_ingestion import DocumentIngestor
# from src.multi_document_chat.retrieval import ConversationalRAG

# def test_document_ingestion_and_rag():
#     try:
#         test_files = [
#             "/Users/benudhorangom/Documents/document_portal/data/multi_doc_chat/market_analysis_report.docx",
#             "/Users/benudhorangom/Documents/document_portal/data/multi_doc_chat/NIPS-2017-attention-is-all-you-need-Paper.pdf",
#             "/Users/benudhorangom/Documents/document_portal/data/multi_doc_chat/sample.pdf",
#             "/Users/benudhorangom/Documents/document_portal/data/multi_doc_chat/state_of_the_union.txt"
#         ]
        
#         uploaded_files = []
        
#         for file_path in test_files:
#             if Path(file_path).exists():
#                 uploaded_files.append(open(file_path, "rb"))
#             else:
#                 print(f"File does not exist: {file_path}")
                
#         if not uploaded_files:
#             print("No valid files to upload.")
#             sys.exit(1)
            
#         ingestor = DocumentIngestor()
        
#         retriever = ingestor.ingest_files(uploaded_files)
        
#         for f in uploaded_files:
#             f.close()
                
#         session_id = "test_multi_doc_chat"
        
#         rag = ConversationalRAG(session_id=session_id, retriever=retriever)
        
#         question = "what is President Zelenskyy said in their speech in parliament?"
        
#         answer=rag.invoke(question)
        
#         print("\n Question:", question)
        
#         print("Answer:", answer)
        
#         if not uploaded_files:
#             print("No valid files to upload.")
#             sys.exit(1)
            
#     except Exception as e:
#         print(f"Test failed: {str(e)}")
#         sys.exit(1)
        
# if __name__ == "__main__":
#     test_document_ingestion_and_rag()
    
