import chromadb
import numpy as np
import torch
import gc
import uuid
import os
from sentence_transformers import SentenceTransformer
import config

class EmbeddingService:
    def __init__(self):
        """Initialize the embedding service with ChromaDB 1.0.12"""
        self.device = config.DEVICE
        print(f"Initializing embedding model on {self.device}")
        
        # Initialize embedding model
        self.model = SentenceTransformer(
            config.EMBEDDING_MODEL,
            device=self.device
        )
        
        # Make sure database directory exists
        os.makedirs(config.CHROMA_DB_DIR, exist_ok=True)
        
        # Initialize ChromaDB client (updated for newer API)
        self.client = chromadb.PersistentClient(path=str(config.CHROMA_DB_DIR))
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection("documents")
            count = self.collection.count()
            print(f"Connected to existing collection with {count} documents")
        except:
            self.collection = self.client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}  # Using cosine similarity
            )
            print("Created new collection 'documents'")
    
    def embed_texts(self, texts):
        """Generate embeddings for a list of texts with batch processing"""
        all_embeddings = []
        batch_size = config.EMBEDDING_BATCH_SIZE
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            # Generate embeddings for the batch
            with torch.no_grad():
                embeddings = self.model.encode(batch_texts, convert_to_numpy=True)
                all_embeddings.extend(embeddings.tolist())
            
            # Clear CUDA cache after each batch
            if config.CLEAR_CUDA_CACHE and torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
        
        return all_embeddings
    
    def add_documents(self, texts, metadatas):
        """Add documents to the vector database with batched processing"""
        if not texts or len(texts) == 0:
            return 0
            
        # Generate embeddings
        embeddings = self.embed_texts(texts)
        
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
    
    def query(self, query_text, n_results=3):
        """Query the vector database for similar documents"""
        # Generate query embedding
        query_embedding = self.model.encode(query_text, convert_to_numpy=True).tolist()
        
        # Query database (updated for newer API)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        # Clear CUDA cache after query
        if config.CLEAR_CUDA_CACHE and torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
        
        return documents, metadatas