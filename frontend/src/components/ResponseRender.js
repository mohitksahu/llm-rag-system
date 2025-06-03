import React from 'react';
import ReactMarkdown from 'react-markdown';

const ResponseRenderer = ({ content }) => {
  return (
    <ReactMarkdown>
      {content}
    </ReactMarkdown>
  );
};

export default ResponseRenderer;