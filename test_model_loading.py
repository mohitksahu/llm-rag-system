#!/usr/bin/env python3
"""
Test script to verify that the LLM model loads correctly after dependency upgrades
"""

import sys
import os
import traceback

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_model_loading():
    """Test if the model can be loaded and moved to CUDA device successfully"""
    print("=" * 60)
    print("Testing LLM Model Loading After Dependency Upgrade")
    print("=" * 60)
    
    try:
        # Import necessary modules
        print("1. Importing modules...")
        import torch
        import bitsandbytes as bnb
        from services.llm_service import LLMService
        
        print(f"   ✓ PyTorch version: {torch.__version__}")
        print(f"   ✓ CUDA available: {torch.cuda.is_available()}")
        print(f"   ✓ bitsandbytes version: {bnb.__version__}")
        
        if torch.cuda.is_available():
            print(f"   ✓ CUDA device: {torch.cuda.get_device_name()}")
            print(f"   ✓ CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        print("\n2. Initializing LLM Service...")
        llm_service = LLMService()
        
        print("\n3. Testing model device placement...")
        # Check if model is properly loaded on device
        if hasattr(llm_service.model, 'device'):
            print(f"   ✓ Model device: {llm_service.model.device}")
        else:
            # For models with device_map="auto", check the first parameter
            first_param = next(llm_service.model.parameters())
            print(f"   ✓ Model device: {first_param.device}")
        
        print("\n4. Testing a simple generation...")
        test_prompt = "Hello, how are you?"
        response = llm_service.generate_response(test_prompt, max_new_tokens=20)
        print(f"   ✓ Test prompt: {test_prompt}")
        print(f"   ✓ Generated response: {response}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED! Model loading is working correctly.")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("\n" + "=" * 60)
        print("❌ TESTS FAILED! There are still issues to resolve.")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_model_loading()
    sys.exit(0 if success else 1)
