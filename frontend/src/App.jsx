import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import DocumentUploader from './components/DocumentUploader';
import './styles/main.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Student RAG Assistant</h1>
        <div className="tab-container">
          <button 
            className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            Ask Questions
          </button>
          <button 
            className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            Upload Sources
          </button>
        </div>
      </header>
      
      <main className="main-content">
        {activeTab === 'chat' ? (
          <ChatInterface />
        ) : (
          <DocumentUploader />
        )}
      </main>
      
      <footer className="app-footer">
        <p>Powered by LLaMA & LangChain | Running on local GPU</p>
      </footer>
    </div>
  );
}

export default App;