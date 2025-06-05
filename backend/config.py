import os
from pathlib import Path

# Find the project root directory
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Flask settings
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Path settings
DATA_DIR = PROJECT_ROOT / 'data'
UPLOAD_FOLDER = DATA_DIR / 'uploaded'
CHROMA_DB_DIR = DATA_DIR / 'chroma_db'

# Ensure directories exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# Model settings - auto-detect and support both CPU and GPU
import sys
import torch

# Check if running in Google Colab
IN_COLAB = 'google.colab' in sys.modules

# Auto-detect device capabilities
def get_device_config():
    if torch.cuda.is_available() and not IN_COLAB:
        # Local GPU environment
        return {
            "device": "cuda",
            "use_quantization": True,
            "model_name": "meta-llama/Llama-2-7b-chat-hf"
        }
    elif torch.cuda.is_available() and IN_COLAB:
        # Colab GPU environment (may have quantization issues)
        return {
            "device": "cuda", 
            "use_quantization": False,  # Disable quantization in Colab
            "model_name": "microsoft/DialoGPT-medium"  # Smaller model for Colab
        }
    else:
        # CPU environment
        return {
            "device": "cpu",
            "use_quantization": False,
            "model_name": "microsoft/DialoGPT-medium"  # Smaller model for CPU
        }

# Get device configuration
device_config = get_device_config()

MODEL_NAME = device_config["model_name"]
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
USE_GPU = device_config["device"] == "cuda"
DEVICE = device_config["device"]
USE_QUANTIZATION = device_config["use_quantization"]

print(f"🔧 Device Configuration:")
print(f"   - Device: {DEVICE}")
print(f"   - Model: {MODEL_NAME}")
print(f"   - Quantization: {USE_QUANTIZATION}")
print(f"   - In Colab: {IN_COLAB}")

# Memory optimization settings
QUANTIZATION = "4bit"
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_INPUT_LENGTH = 512
EMBEDDING_BATCH_SIZE = 8
CHUNK_SIZE = 600
CHUNK_OVERLAP = 50
CLEAR_CUDA_CACHE = True