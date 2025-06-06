import torch
import gc
import config
import os
import sys
from huggingface_hub import login
from utils.env_utils import load_environment

# Dynamic imports based on availability
try:
    from transformers import BitsAndBytesConfig
    QUANTIZATION_AVAILABLE = True
except ImportError:
    QUANTIZATION_AVAILABLE = False
    print("Warning: BitsAndBytesConfig not available, quantization disabled")

from transformers import AutoTokenizer, AutoModelForCausalLM


class LLMService:
    def __init__(self):
        """Initialize the LLM service with automatic device detection"""
        print(f"Initializing LLM on {config.DEVICE}")
        print(f"Model: {config.MODEL_NAME}")
        print(f"Quantization enabled: {config.USE_QUANTIZATION}")

        # Load environment variables
        load_environment()

        # Get token from .env file
        token = os.getenv("HUGGINGFACE_TOKEN")
        if token:
            print("Using token from .env file")
            try:
                login(token=token)
                print("Login successful")
            except Exception as e:
                print(f"Login failed: {e}")
        else:
            print("Warning: No Hugging Face token found in .env file")

        # Initialize tokenizer and model
        self._load_model(token)

    def _load_model(self, token):
        """Load the model with appropriate configuration for the device"""
        try:
            # Load tokenizer
            print("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                config.MODEL_NAME,
                token=token if token else None,
                trust_remote_code=True
            )
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

            # Prepare model loading arguments
            model_kwargs = {
                "pretrained_model_name_or_path": config.MODEL_NAME,
                "torch_dtype": torch.float16 if config.USE_GPU else torch.float32,
                "trust_remote_code": True,
                "low_cpu_mem_usage": True
            }

            if token:
                model_kwargs["token"] = token

            # Configure device mapping and quantization
            if config.USE_QUANTIZATION and QUANTIZATION_AVAILABLE:
                print("Configuring 4-bit quantization...")
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16 if config.USE_GPU else torch.float32
                )
                model_kwargs["quantization_config"] = quantization_config
                if config.USE_GPU and torch.cuda.is_available():
                    model_kwargs["device_map"] = "auto"
                    if not config.IN_COLAB:
                        model_kwargs["max_memory"] = {0: "5GiB"}
                else:
                    model_kwargs["device_map"] = {"": "cpu"}
            else:
                print("Quantization disabled or not available - loading model in full precision")
                if config.USE_GPU and torch.cuda.is_available():
                    model_kwargs["device_map"] = "auto"
                    if not config.IN_COLAB:
                        model_kwargs["max_memory"] = {0: "5GiB"}
                else:
                    model_kwargs["device_map"] = {"": "cpu"}

            # Load model
            print("Loading model (this may take a few minutes)...")
            self.model = AutoModelForCausalLM.from_pretrained(**model_kwargs)

            # Move to device if not using device_map
            if not config.USE_GPU or not torch.cuda.is_available():
                self.device = "cpu"
                self.model = self.model.to("cpu")
            else:
                self.device = "cuda"

            print(f"✓ Model loaded successfully on {self.device}!")

        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise RuntimeError("Failed to load the Llama model. Please check your environment and dependencies.")

    def generate_response(self, prompt, max_new_tokens=None):
        """Generate a response from the LLM given a prompt"""
        if max_new_tokens is None:
            max_new_tokens = config.MAX_NEW_TOKENS

        # Enforce input length limit for memory optimization
        if hasattr(config, 'MAX_INPUT_LENGTH'):
            prompt = prompt[-config.MAX_INPUT_LENGTH:]

        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=1024
            )

            # Move inputs to the correct device
            if hasattr(self, 'device'):
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            elif config.USE_GPU and torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=config.TEMPERATURE,
                    top_p=config.TOP_P,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )

            # Extract the newly generated text (excluding the prompt)
            response = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )

            # Clear CUDA cache if configured and available
            if (hasattr(config, 'CLEAR_CUDA_CACHE') and
                    config.CLEAR_CUDA_CACHE and
                    torch.cuda.is_available()):
                torch.cuda.empty_cache()
                gc.collect()

            return response.strip()

        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"

    def get_model_info(self):
        """Get information about the loaded model"""
        return {
            "model_name": config.MODEL_NAME,
            "device": getattr(self, 'device', config.DEVICE),
            "use_gpu": config.USE_GPU,
            "use_quantization": config.USE_QUANTIZATION,
            "in_colab": config.IN_COLAB,
            "cuda_available": torch.cuda.is_available(),
            "quantization_available": QUANTIZATION_AVAILABLE
        }
