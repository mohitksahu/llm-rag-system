import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings
import torch
import config
import uuid

class EmbeddingService:
    def __init__(self):
        """Initialize the embedding service"""
        self.device = config.DEVICE
        
        # Initialize embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"device": self.device}
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create a collection if it doesn't exist
        try:
            self.collection = self.client.get_collection("documents")
        except:
            self.collection = self.client.create_collection("documents")
    
    def add_documents(self, texts, metadatas):
        """Add documents to the vector database"""
        if not texts or len(texts) == 0:
            return 0
            
        # Generate embeddings
        embeddings = [self.embeddings.embed_query(text) for text in texts]
        
        # Generate unique IDs
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(texts)
    
    def query(self, query_text, n_results=5):
        """Query the vector database for similar documents"""
        query_embedding = self.embeddings.embed_query(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        return documents, metadatas