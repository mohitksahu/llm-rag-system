import React from 'react';

const SourcesDisplay = ({ sources }) => {
  // Group sources by filename to avoid repetition
  const groupedSources = sources.reduce((acc, source) => {
    if (!acc[source.source]) {
      acc[source.source] = [];
    }
    acc[source.source].push(source);
    return acc;
  }, {});
  
  return (
    <div className="sources-display">
      <h4>Referenced Sources</h4>
      <ul className="sources-list">
        {Object.entries(groupedSources).map(([filename, sourceGroup], index) => (
          <li key={index} className="source-item">
            <div className="source-file">
              <span className="source-icon">
                {sourceGroup[0].type === 'pdf' ? '📄' : '🖼️'}
              </span>
              <span className="source-name">{filename}</span>
            </div>
            <span className="source-type">{sourceGroup[0].type}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SourcesDisplay;