"""Debug script to diagnose LLM service issues."""
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from services.llm_service import LLMService
from utils.env_utils import load_environment

def debug_llm():
    """Debug the LLM service."""
    # Load environment variables
    print("Loading environment variables...")
    load_environment()
    
    # Initialize LLM service
    print("Initializing LLM service...")
    llm = LLMService()
    
    # Test prompt
    test_prompt = "Explain what RAG means in AI"
    print(f"Sending test prompt: '{test_prompt}'")
    
    # Get the raw tokenizer output
    print("\nDEBUG - Raw tokenizer output:")
    tokenizer = llm.tokenizer
    tokens = tokenizer(test_prompt, return_tensors="pt")
    print(f"Type of tokens: {type(tokens)}")
    print(f"Keys in tokens: {tokens.keys()}")
    print(f"tokens['input_ids'] shape: {tokens['input_ids'].shape}")
    
    # Try the prediction
    try:
        response = llm.generate(test_prompt)
        print(f"\nSuccess! Response: {response}")
    except Exception as e:
        print(f"\nError in generate method: {str(e)}")
        print("\nTraceback:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_llm()
