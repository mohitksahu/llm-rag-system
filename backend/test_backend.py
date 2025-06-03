from services.llm_service import LLMService
from services.embedding_service import EmbeddingService
from services.rag_pipeline import RAGPipeline
from utils.env_utils import load_environment

def test_backend():
    print("Testing backend components...")
    
    # Load environment variables
    load_environment()
    
    # Test LLM service
    print("\n--- Testing LLM Service ---")
    llm = LLMService()
    test_prompt = "Explain what RAG means in AI"
    print(f"Sending test prompt: '{test_prompt}'")
    response = llm.generate_response(test_prompt)
    print(f"Response: {response[:100]}...")  # Show first 100 chars
    
    # Test Embedding service
    print("\n--- Testing Embedding Service ---")
    embed_service = EmbeddingService()
    test_texts = ["This is a test document about artificial intelligence."]
    test_metadata = [{"source": "test.txt", "type": "text"}]
    print("Adding test document to vector database...")
    embed_service.add_documents(test_texts, test_metadata)
    
    # Test RAG pipeline
    print("\n--- Testing RAG Pipeline ---")
    rag = RAGPipeline(llm)
    test_query = "What is artificial intelligence?"
    print(f"Sending query to RAG pipeline: '{test_query}'")
    result, sources = rag.process_query(test_query)
    print(f"Response: {result[:100]}...")
    print(f"Sources: {sources}")
    
    print("\nBackend test completed!")

if __name__ == "__main__":
    test_backend()