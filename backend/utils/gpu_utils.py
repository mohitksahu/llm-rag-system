import torch

def get_gpu_info():
    """Get current GPU information"""
    if not torch.cuda.is_available():
        return {"available": False, "message": "CUDA is not available"}
    
    try:
        device_count = torch.cuda.device_count()
        current_device = torch.cuda.current_device()
        device_name = torch.cuda.get_device_name(current_device)
        memory_allocated = torch.cuda.memory_allocated(current_device) / (1024 ** 3)  # GB
        memory_reserved = torch.cuda.memory_reserved(current_device) / (1024 ** 3)  # GB
        
        return {
            "available": True,
            "device_count": device_count,
            "current_device": current_device,
            "device_name": device_name,
            "memory_allocated_gb": round(memory_allocated, 2),
            "memory_reserved_gb": round(memory_reserved, 2)
        }
    except Exception as e:
        return {"available": False, "message": str(e)}