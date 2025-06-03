from services.embedding_service import EmbeddingService
import torch
import gc
import config

class RAGPipeline:
    def __init__(self, llm_service):
        """Initialize the RAG pipeline"""
        self.llm_service = llm_service
        self.embedding_service = EmbeddingService()
    
    def process_query(self, query):
        """Process a query through the RAG pipeline"""
        # Retrieve relevant documents
        documents, metadatas = self.embedding_service.query(query, n_results=3)
        
        # Format context from retrieved documents
        context_parts = []
        for i, doc in enumerate(documents):
            # Truncate long documents
            if len(doc) > 300:
                doc = doc[:300] + "..."
            context_parts.append(f"Document {i+1}: {doc}")
        
        context = "\n\n".join(context_parts)
        
        # Format prompt for Llama 2
        prompt = f"""You are a helpful educational assistant. Use only the following context to answer the student's question. If you don't know the answer based on the context, say that you don't have enough information.

Context:
{context}

Student Question: {query}

Helpful Answer:"""
        
        # Generate response
        response = self.llm_service.generate_response(prompt)
        
        # Format sources for citation
        sources = [
            {
                "source": metadata["source"],
                "type": metadata["type"]
            } for metadata in metadatas
        ]
        
        # Clear CUDA cache after processing
        if config.CLEAR_CUDA_CACHE and torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
        
        return response, sources
