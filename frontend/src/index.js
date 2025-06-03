import React from 'react';
import { createRoot } from 'react-dom/client'; // Note this updated import
import './index.css';
import App from './App';

// Wait for DOM to be fully loaded
const container = document.getElementById('root');

// Check if container exists before mounting
if (container) {
  const root = createRoot(container);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("Cannot find element with id 'root'");
}