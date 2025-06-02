import React, { useState } from 'react';
import SourcesDisplay from './SourcesDisplay';

const ResponseDisplay = ({ content, sources, error, processingTime }) => {
  const [showSources, setShowSources] = useState(false);
  
  if (error) {
    return (
      <div className="response-display error">
        <div className="response-content">{content}</div>
      </div>
    );
  }
  
  return (
    <div className="response-display">
      <div className="response-content">{content}</div>
      
      <div className="response-footer">
        {processingTime && (
          <span className="processing-time">
            Generated in {processingTime}s
          </span>
        )}
        
        {sources && sources.length > 0 && (
          <div className="sources-section">
            <button
              className="sources-toggle"
              onClick={() => setShowSources(!showSources)}
            >
              {showSources ? 'Hide Sources' : 'Show Sources'} ({sources.length})
            </button>
            
            {showSources && <SourcesDisplay sources={sources} />}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResponseDisplay;