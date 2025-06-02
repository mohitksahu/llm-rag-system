from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import gc
import config
import os
from huggingface_hub import login
from utils.env_utils import load_environment

class LLMService:
    def __init__(self):
        """Initialize the LLM service with Llama 2"""
        self.device = config.DEVICE
        print(f"Initializing Llama 2 on {self.device}")
        
        # Load environment variables
        load_environment()
        
        # Get token from .env file
        token = os.getenv("HUGGINGFACE_TOKEN")
        if token:
            print("Using token from .env file")
            login(token=token)
        else:
            print("Warning: No Hugging Face token found in .env file")
        
        # Configure quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16
        )
        
        # Load tokenizer and model
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            config.MODEL_NAME,
            use_auth_token=token
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("Loading model (this may take a few minutes)...")
        self.model = AutoModelForCausalLM.from_pretrained(
            config.MODEL_NAME,
            device_map="auto",
            quantization_config=quantization_config,
            torch_dtype=torch.float16,
            max_memory={0: "5GiB"},
            use_auth_token=token
        )
        print("Model loaded successfully!")
        
    def generate_response(self, prompt, max_new_tokens=None):
        """Generate a response from the LLM given a prompt"""
        if max_new_tokens is None:
            max_new_tokens = config.MAX_NEW_TOKENS
            
        # Enforce input length limit for memory optimization
        if hasattr(config, 'MAX_INPUT_LENGTH'):
            prompt = prompt[-config.MAX_INPUT_LENGTH:]
            
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P,
            )
        
        # Extract the newly generated text (excluding the prompt)
        response = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        
        # Clear CUDA cache if configured
        if hasattr(config, 'CLEAR_CUDA_CACHE') and config.CLEAR_CUDA_CACHE and torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()
            
        return response