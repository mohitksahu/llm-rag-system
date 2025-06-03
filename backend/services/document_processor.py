import os
import PyPDF2
from PIL import Image
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.embedding_service import EmbeddingService
import torch
import gc
import config

class DocumentProcessor:
    def __init__(self):
        """Initialize the document processor"""
        self.embedding_service = EmbeddingService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def process(self, file_path, document_type):
        """Process a document based on its type"""
        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        if file_size_mb > 50:  # 50MB limit
            raise ValueError(f"File too large ({file_size_mb:.1f}MB). Maximum size is 50MB.")
            
        if document_type == 'pdf':
            return self.process_pdf(file_path)
        elif document_type in ['jpg', 'jpeg', 'png', 'gif']:
            return self.process_image(file_path)
        else:
            raise ValueError(f"Unsupported document type: {document_type}")
    
    def process_pdf(self, file_path):
        """Process PDF with memory management"""
        processed_chunks = 0
        file_name = os.path.basename(file_path)
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Process in batches of 5 pages
            batch_size = 5
            total_pages = len(pdf_reader.pages)
            
            for batch_start in range(0, total_pages, batch_size):
                batch_end = min(batch_start + batch_size, total_pages)
                batch_text = ""
                
                for i in range(batch_start, batch_end):
                    text = pdf_reader.pages[i].extract_text()
                    if text:
                        batch_text += f"Page {i+1}:\n{text}\n\n"
                
                if batch_text:
                    chunks = self.text_splitter.split_text(batch_text)
                    
                    # Prepare metadata for each chunk
                    metadatas = [{
                        "source": file_name,
                        "type": "pdf",
                        "page_range": f"{batch_start+1}-{batch_end}"
                    } for _ in chunks]
                    
                    # Add chunks to the embedding database
                    processed_chunks += self.embedding_service.add_documents(chunks, metadatas)
                      # Clear cache to free memory
                    if config.CLEAR_CUDA_CACHE and torch.cuda.is_available():
                        torch.cuda.empty_cache()
                        gc.collect()
        
        return processed_chunks
    
    def process_image(self, file_path):
        """Extract text from image using OCR and add to vector database"""
        file_name = os.path.basename(file_path)
        
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            if text.strip():
                chunks = self.text_splitter.split_text(text)
                
                metadatas = [{
                    "source": file_name,
                    "type": "image"
                } for _ in chunks]
                
                return self.embedding_service.add_documents(chunks, metadatas)
            
            return 0
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")