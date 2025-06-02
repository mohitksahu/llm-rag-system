"""Test the Hugging Face token."""
from utils.env_utils import load_environment
import os
from huggingface_hub import HfApi

def test_token():
    # Load environment variables
    load_environment()
    
    # Get token
    token = os.getenv("HUGGINGFACE_TOKEN")
    if not token:
        print("❌ Error: HUGGINGFACE_TOKEN not found in .env file")
        return False
    
    # Test token
    try:
        api = HfApi(token=token)
        user_info = api.whoami()
        print(f"✓ Successfully authenticated as: {user_info['name']}")
        
        # Test if we can access the Llama model
        print("Checking access to Llama 2...")
        model_info = api.model_info("meta-llama/Llama-2-7b-chat-hf")
        print(f"✓ You have access to: {model_info.modelId}")
        print("✓ Your token is valid and has proper permissions!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_token()