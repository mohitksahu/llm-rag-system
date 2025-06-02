import os
import PyPDF2
from PIL import Image
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.embedding_service import EmbeddingService

class DocumentProcessor:
    def __init__(self):
        """Initialize the document processor"""
        self.embedding_service = EmbeddingService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def process(self, file_path, document_type):
        """Process a document based on its type"""
        if document_type == 'pdf':
            return self.process_pdf(file_path)
        elif document_type in ['jpg', 'jpeg', 'png', 'gif']:
            return self.process_image(file_path)
        else:
            raise ValueError(f"Unsupported document type: {document_type}")
    
    def process_pdf(self, file_path):
        """Extract text from PDF, chunk it and add to vector database"""
        full_text = ""
        file_name = os.path.basename(file_path)
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text:
                    full_text += f"Page {i+1}:\n{text}\n\n"
        
        # Split text into chunks
        if full_text.strip():
            chunks = self.text_splitter.split_text(full_text)
            
            # Prepare metadata for each chunk
            metadatas = [{
                "source": file_name,
                "type": "pdf"
            } for _ in chunks]
            
            # Add chunks to the embedding database
            return self.embedding_service.add_documents(chunks, metadatas)
        
        return 0
    
    def process_image(self, file_path):
        """Extract text from image using OCR and add to vector database"""
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        file_name = os.path.basename(file_path)
        
        if text.strip():
            chunks = self.text_splitter.split_text(text)
            
            metadatas = [{
                "source": file_name,
                "type": "image"
            } for _ in chunks]
            
            return self.embedding_service.add_documents(chunks, metadatas)
        
        return 0