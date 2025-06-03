import React from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './styles/App.css';
import ChatInterface from './components/ChatInterface';
import Footer from './components/Footer';

function App() {
  return (
    <div className="app">
      {/* Translucent Navbar */}      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-brand">
            <span className="brand-icon">🪶</span>
            <span className="brand-text">QueryQuill</span>
            <span className="assistant-text">Assistant</span>
          </div>
        </div>
      </nav>{/* Main Content */}
      <main className="main-content">
        <div className="content-container">
          <div className="tab-content">
            <div className="tab-pane active">
              <ChatInterface />
            </div>
          </div>
        </div>
      </main>      <Footer />

      <ToastContainer
        position="bottom-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </div>
  );
}

export default App;