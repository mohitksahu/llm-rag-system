"""Utility functions for environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file."""
    # Find the project root directory (location of .env file)
    # Start from current directory and move up until we find it
    current_dir = Path(__file__).parent
    project_root = current_dir
    
    # Look up to 3 levels up for the .env file
    for _ in range(3):
        if (project_root / '.env').exists():
            break
        project_root = project_root.parent
    
    # Load the .env file
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    
    # Verify token is loaded
    token = os.getenv('HUGGINGFACE_TOKEN')
    if not token:
        print("Warning: HUGGINGFACE_TOKEN not found in .env file")
    else:
        print("✓ Environment variables loaded successfully")
        
    return token is not None
