import React, { useState, useRef, useEffect } from 'react';
import { toast } from 'react-toastify';
import { sendQuery, uploadDocument } from '../services/api';
import Message from './Message';
import '../styles/ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false); const [isUploading, setIsUploading] = useState(false);
  // eslint-disable-next-line no-unused-vars
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleFileUpload = async (file) => {
    const allowedTypes = [
      'application/pdf',
      'image/jpeg',
      'image/png',
      'image/jpg'
    ];

    if (!allowedTypes.includes(file.type)) {
      toast.error('Only PDF and image files (JPG, PNG) are supported');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      toast.error('File size must be less than 50MB');
      return;
    }

    setIsUploading(true);

    try {
      const result = await uploadDocument(file);

      setUploadedFiles((prev) => [
        ...prev,
        {
          name: file.name,
          uploadedAt: new Date().toISOString(),
          type: file.type,
          chunks: result.chunks_processed
        }
      ]);

      toast.success(`Successfully processed ${file.name} (${result.chunks_processed} chunks extracted)`);
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(`Failed to process ${file.name}. ${error.message || 'Please try again.'}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await sendQuery(inputValue);

      const assistantMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        sources: response.sources,
        processingTime: response.processing_time
      };

      setMessages((prevMessages) => [...prevMessages, assistantMessage]);

    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to get response. Please try again.');

      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  return (<div className="chat-interface glass-card">      <div className="chat-header">
    <div className="chat-status">
      {isLoading && (
        <div className="status-indicator loading">
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span>Thinking...</span>
        </div>
      )}
      {isUploading && (
        <div className="status-indicator uploading">
          <span>📄</span>
          <span>Uploading...</span>
        </div>
      )}
    </div>
  </div><div className="messages-container">
      {uploadedFiles.length > 0 && (
        <div className="uploaded-files-container">
          <div className="uploaded-files-header">
            <span className="files-icon">📚</span>
            <span>Uploaded Documents</span>
            <span className="files-count">{uploadedFiles.length}</span>
          </div>
          <div className="uploaded-files-list">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="uploaded-file-item">
                <span className="file-type-icon">
                  {file.type.includes('pdf') ? '📄' : '🖼️'}
                </span>
                <span className="file-name">{file.name}</span>
                <span className="file-chunks">{file.chunks} chunks</span>
              </div>
            ))}
          </div>
        </div>
      )}
      {messages.length === 0 ? (<div className="welcome-screen">          <div className="welcome-icon">🪶</div>
        <h3>Welcome</h3>
        <p>Upload docs for insights</p>
        <div className="features-summary">
          <div className="feature-item">
            <span className="feature-icon">📊</span>
            <span>Analysis</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🔍</span>
            <span>Context</span>
          </div>
        </div>
        <div className="example-grid">
          <div className="example-card" onClick={() => setInputValue("Summarize")}>
            <span className="example-icon">📋</span>
            <span>Summarize</span>
          </div>
          <div className="example-card" onClick={() => setInputValue("Key points?")}>
            <span className="example-icon">💡</span>
            <span>Key points</span>
          </div>
          <div className="example-card" onClick={() => setInputValue("Explain")}>
            <span className="example-icon">🎓</span>
            <span>Explain</span>
          </div>
        </div>
      </div>
      ) : (
        <div className="messages-list">
          {messages.map((message) => (
            <Message key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="typing-indicator">
              <div className="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span className="typing-text">AI is thinking...</span>
            </div>
          )}
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>      <form className="chat-input-form" onSubmit={handleSubmit}>
      <div className="input-container">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        <button
          type="button"
          className="upload-button"
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          title="Upload document"
        >
          {isUploading ? '⏳' : '📎'}
        </button>          <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask me anything..."
          className="chat-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="send-button btn-primary"
          disabled={isLoading || !inputValue.trim()}
        >
          <span className="send-icon">
            {isLoading ? '⏳' : '🚀'}
          </span>
        </button>
      </div>
    </form>
  </div>
  );
};

export default ChatInterface;