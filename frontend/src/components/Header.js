import React from 'react';
import '../styles/Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <h1>Llama RAG System</h1>
        <p>Powered by Llama 2 & Retrieval Augmented Generation</p>
      </div>
    </header>
  );
};

export default Header;