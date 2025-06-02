import os

# Flask settings
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Path settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploaded')
CHROMA_DB_DIR = os.path.join(DATA_DIR, 'chroma_db')

# Model settings - optimized for RTX 3050 6GB
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
USE_GPU = True
DEVICE = "cuda" if USE_GPU else "cpu"

# Memory optimization settings
QUANTIZATION = "4bit"
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_INPUT_LENGTH = 1024  # Limit input context to save memory
EMBEDDING_BATCH_SIZE = 16
CHUNK_SIZE = 800  # Smaller chunks for better memory management
CHUNK_OVERLAP = 100
CLEAR_CUDA_CACHE = True  # Enable cache clearing between operations