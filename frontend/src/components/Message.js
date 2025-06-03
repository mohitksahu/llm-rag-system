import React from 'react';
import ResponseRenderer from './ResponseRender';
import SourceCitation from './SourceCitation';
import '../styles/Message.css';

const Message = ({ message }) => {
  const { text, sender, sources, processingTime, isError } = message;

  // Format timestamp
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message ${sender}-message ${isError ? 'error-message' : ''}`}>
      <div className="message-content">
        {sender === 'user' ? (
          <p>{text}</p>
        ) : (
          <ResponseRenderer content={text} />
        )}
      </div>

      {sources && sources.length > 0 && (
        <SourceCitation sources={sources} />
      )}

      {processingTime && (
        <div className="processing-time">
          Generated in {processingTime} seconds
        </div>
      )}

      <div className="message-timestamp">
        {formatTime(message.timestamp)}
      </div>
    </div>
  );
};

export default Message;