import React, { useState } from 'react';
import '../styles/SourceCitation.css';

const SourceCitation = ({ sources }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  if (!sources || sources.length === 0) return null;
  
  return (
    <div className="source-citation">
      <button 
        className="source-toggle" 
        onClick={() => setIsExpanded(!isExpanded)}
      >
        {isExpanded ? 'Hide Sources' : 'Show Sources'} ({sources.length})
      </button>
      
      {isExpanded && (
        <div className="source-list">
          <h4>Sources:</h4>
          <ul>
            {sources.map((source, index) => (
              <li key={index}>
                <strong>{source.source}</strong>
                {source.type && <span className="source-type">{source.type}</span>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SourceCitation;