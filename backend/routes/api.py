from flask import Blueprint, request, jsonify
from services.llm_service import LLMService
from services.document_processor import DocumentProcessor
from services.rag_pipeline import RAGPipeline
import os
import config
import time
import torch

# Initialize services
api_bp = Blueprint('api', __name__)

# Lazy initialization to save memory
llm_service = None
document_processor = None
rag_pipeline = None

def get_llm_service():
    global llm_service
    if llm_service is None:
        llm_service = LLMService()
    return llm_service

def get_document_processor():
    global document_processor
    if document_processor is None:
        document_processor = DocumentProcessor()
    return document_processor

def get_rag_pipeline():
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline(get_llm_service())
    return rag_pipeline

@api_bp.route('/query', methods=['POST'])
def query():
    """API endpoint for querying the RAG model"""
    start_time = time.time()
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        # Clear GPU cache before processing new query
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        pipeline = get_rag_pipeline()
        response, sources = pipeline.process_query(query)
        processing_time = time.time() - start_time
        
        return jsonify({
            "response": response,
            "sources": sources,
            "processing_time": round(processing_time, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/upload', methods=['POST'])
def upload_document():
    """API endpoint for uploading and processing documents"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Clear GPU cache before processing new document
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        # Save file to uploads directory
        file_path = os.path.join(str(config.UPLOAD_FOLDER), file.filename)
        file.save(file_path)
        
        document_type = file.filename.split('.')[-1].lower()
        processor = get_document_processor()
        processed_chunks = processor.process(file_path, document_type)
        
        return jsonify({
            "success": True,
            "message": f"File {file.filename} uploaded and processed successfully",
            "chunks_processed": processed_chunks
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/status', methods=['GET'])
def status():
    """API endpoint for checking server status"""
    gpu_available = torch.cuda.is_available()
    gpu_info = {}
    
    if gpu_available:
        gpu_info = {
            "device_count": torch.cuda.device_count(),
            "current_device": torch.cuda.current_device(),
            "device_name": torch.cuda.get_device_name(0),
            "memory_allocated_mb": round(torch.cuda.memory_allocated() / (1024 ** 2), 2),
            "memory_reserved_mb": round(torch.cuda.memory_reserved() / (1024 ** 2), 2)
        }
    
    return jsonify({
        "status": "online",
        "gpu_available": gpu_available,
        "gpu_info": gpu_info,
        "model_name": config.MODEL_NAME,
        "embedding_model": config.EMBEDDING_MODEL
    })