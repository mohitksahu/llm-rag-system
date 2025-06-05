import torch
import sys

print(f"PyTorch version: {torch.__version__}")
print(f"Python version: {sys.version}")
print("\nAvailable devices:")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device count: {torch.cuda.device_count()}")
    print(f"CUDA device name: {torch.cuda.get_device_name(0)}")

# Check for other potential devices
try:
    import torch_npu  # This would be needed for Huawei NPU
    print(f"NPU available: {torch_npu.is_available()}")
except ImportError:
    print("NPU support not installed")
    
try:
    # Check for Intel XPU (formerly known as Intel GPU)
    import intel_extension_for_pytorch as ipex
    print(f"Intel XPU/GPU available: {ipex.xpu.is_available()}")
except ImportError:
    print("Intel XPU support not installed")

# Check all available devices through bitsandbytes if installed
try:
    import bitsandbytes as bnb
    print("\nBitsandbytes information:")
    print(f"bitsandbytes version: {bnb.__version__}")
    try:
        print(f"Supported devices: {bnb.AVAILABLE_DEVICES}")
    except AttributeError:
        print("Could not retrieve supported devices information")
except ImportError:
    print("\nbitsandbytes not installed")
