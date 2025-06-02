from flask import Blueprint, request, jsonify
from services.llm_service import LLMService
from services.document_processor import DocumentProcessor
from services.rag_pipeline import RAGPipeline
import os
import config
import time

api_bp = Blueprint('api', __name__)
llm_service = LLMService()
document_processor = DocumentProcessor()
rag_pipeline = RAGPipeline(llm_service)

@api_bp.route('/query', methods=['POST'])
def query():
    """API endpoint for querying the RAG model"""
    start_time = time.time()
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        response, sources = rag_pipeline.process_query(query)
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
        file_path = os.path.join(config.UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        document_type = file.filename.split('.')[-1].lower()
        processed_chunks = document_processor.process(file_path, document_type)
        
        return jsonify({
            "success": True,
            "message": f"File {file.filename} uploaded and processed successfully",
            "chunks_processed": processed_chunks
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500