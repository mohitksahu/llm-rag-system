from services.embedding_service import EmbeddingService

class RAGPipeline:
    def __init__(self, llm_service):
        """Initialize the RAG pipeline"""
        self.llm_service = llm_service
        self.embedding_service = EmbeddingService()
    
    def process_query(self, query):
        """Process a query through the RAG pipeline"""
        # Retrieve relevant documents
        documents, metadatas = self.embedding_service.query(query)
        
        # Format context from retrieved documents
        context = "\n\n".join([f"Document: {doc}" for doc in documents])
        
        # Format prompt
        prompt = f"""
        You are an educational assistant helping a student with their query. 
        Use only the following context to answer the question. If you don't know the answer based on the context, say so clearly.

        CONTEXT:
        {context}

        QUESTION:
        {query}

        ANSWER:
        """
        
        # Generate response
        response = self.llm_service.generate_response(prompt)
        
        # Format sources for citation
        sources = [
            {
                "source": metadata["source"],
                "type": metadata["type"]
            } for metadata in metadatas
        ]
        
        return response, sources