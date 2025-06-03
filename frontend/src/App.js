import React from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './styles/App.css';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import DocumentUploader from './components/DocumentUploader';
import Footer from './components/Footer';

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <div className="container">
          <div className="row">
            <div className="col-md-4">
              <DocumentUploader />
            </div>
            <div className="col-md-8">
              <ChatInterface />
            </div>
          </div>
        </div>
      </main>
      <Footer />
      <ToastContainer position="bottom-right" />
    </div>
  );
}

export default App;