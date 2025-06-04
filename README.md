# QueryQuill: Llama RAG System

QueryQuill is a full-stack Retrieval-Augmented Generation (RAG) application that leverages LLMs (Large Language Models) for document-based question answering. It features a modern, responsive frontend and a robust Python backend, supporting document upload, semantic search, and conversational chat with context-aware responses.

---

## Features
- **Document Upload & Processing**: Upload PDFs and other documents for ingestion and semantic chunking.
- **RAG Pipeline**: Uses embeddings and vector search to retrieve relevant context for LLM answers.
- **Conversational Chat**: Chat interface with history, example questions, and feature highlights.
- **Modern UI**: Responsive, glassmorphic design with clear boundaries, visible header/footer, and no page scroll.
- **ChromaDB Integration**: Stores and retrieves document embeddings efficiently.
- **Extensible Backend**: Modular Python backend for easy extension and integration.

---

## Tech Stack

### Frontend
- **React** (JavaScript)
- **CSS** (Custom, glassmorphism, responsive design)
- **Tailwind CSS** (utility-first styling)
- **react-toastify** (notifications)

### Backend
- **Python 3.10+**
- **FastAPI** (API server)
- **ChromaDB** (vector database)
- **LangChain** (LLM orchestration)
- **HuggingFace Transformers** (LLM/embedding models)
- **PyTorch** (model backend)

### Other
- **PowerShell** (for Windows shell commands)
- **venv** (Python virtual environments)

---

## Project Structure
```
llama-rag-system/
  backend/         # Python FastAPI backend, RAG pipeline, services
  frontend/        # React frontend (src/, public/, styles/)
  data/            # Uploaded files, ChromaDB storage
  llama-rag-env/   # Python virtual environment
  README.md        # This file
```

---

## Local Development Setup

### 1. Clone the Repository
```powershell
git clone <your-repo-url>
cd llama-rag-system
```

### 2. Set Up Python Backend
```powershell
cd backend
python -m venv ../llama-rag-env
./llama-rag-env-new/Scripts/activate
pip install -r requirements.txt
```

#### 2.1. Run the Backend
```powershell
python app.py
```

### 3. Set Up React Frontend
```powershell
cd ../frontend
npm install
```

#### 3.1. Run the Frontend
```powershell
npm start
```

- The frontend will be available at [http://localhost:3000](http://localhost:3000)
- The backend API will be available at [http://localhost:5000](http://localhost:5000)

---

## Usage
- Upload documents via the UI
- Ask questions in the chat interface
- The system retrieves relevant context and generates answers using the LLM

---

## License
This project is licensed under the MIT License.

---

## Author
- Mohit Kumar Sahu
