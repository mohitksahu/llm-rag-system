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

# Model settings - optimized for RTX 3050 6GB
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
USE_GPU = True
DEVICE = "cuda" if USE_GPU else "cpu"

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