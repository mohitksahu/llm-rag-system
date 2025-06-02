import React, { useState, useRef, useEffect } from 'react';
import ResponseDisplay from './ResponseDisplay';
import { sendQuery } from '../services/api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputValue };
    setMessages([...messages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await sendQuery(inputValue.trim());
      
      const assistantMessage = { 
        role: 'assistant', 
        content: response.response,
        sources: response.sources,
        processingTime: response.processing_time
      };
      
      setMessages(prevMessages => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error('Error getting response:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error while processing your request.',
        error: true
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>Welcome to your Study Assistant!</h2>
            <p>Ask me questions about your uploaded documents. I'll use your sources to provide accurate answers.</p>
            <div className="example-questions">
              <p className="example-header">Example questions:</p>
              <ul>
                <li>"Can you summarize the key points from my uploaded textbook chapter?"</li>
                <li>"What are the main arguments in the research paper I uploaded?"</li>
                <li>"Explain the concept of [topic] based on my lecture notes"</li>
              </ul>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div 
              key={index} 
              className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
            >
              {message.role === 'user' ? (
                <div className="message-content">{message.content}</div>
              ) : (
                <ResponseDisplay 
                  content={message.content} 
                  sources={message.sources}
                  error={message.error}
                  processingTime={message.processingTime}
                />
              )}
            </div>
          ))
        )}
        {isLoading && (
          <div className="message assistant-message">
            <div className="loading-indicator">
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
            </div>
            <div className="loading-text">Processing on local GPU...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="chat-input"
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={isLoading || !inputValue.trim()}
        >
          <span className="send-icon">➤</span>
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;