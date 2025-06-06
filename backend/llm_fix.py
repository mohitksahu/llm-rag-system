"""Fix for the 'dict' object has no attribute 'input_ids' error in LLM service."""

import sys
from pathlib import Path

def main():
    """Fix the LLM service error."""
    # Path to the LLM service file
    llm_service_path = Path(__file__).parent / "services" / "llm_service.py"
    
    if not llm_service_path.exists():
        print(f"Error: LLM service file not found at {llm_service_path}")
        return
    
    # Read the file
    content = llm_service_path.read_text()
    
    # Check if the file needs fixing
    if "inputs.input_ids" in content or "inputs.attention_mask" in content:
        # Fix the code
        content = content.replace("inputs.input_ids", "inputs['input_ids']")
        content = content.replace("inputs.attention_mask", "inputs['attention_mask']")
        
        # Write the fixed content back
        llm_service_path.write_text(content)
        print(f"✅ Fixed LLM service file: {llm_service_path}")
    else:
        print(f"⚠️ No issues found in LLM service file")
    
if __name__ == "__main__":
    main()
