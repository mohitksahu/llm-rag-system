import React, { useState } from 'react';
import { uploadDocument } from '../services/api';

const DocumentUploader = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setStatus(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setStatus({ type: 'info', message: 'Uploading and processing document...' });

    try {
      const response = await uploadDocument(file);
      setStatus({ 
        type: 'success', 
        message: `Document processed successfully! Created ${response.chunks_processed} chunks for retrieval.` 
      });
      setUploadedFiles([...uploadedFiles, { 
        name: file.name, 
        timestamp: new Date(),
        chunks: response.chunks_processed 
      }]);
      setFile(null);
      
      // Reset file input
      e.target.reset();
    } catch (error) {
      console.error('Error uploading document:', error);
      setStatus({ type: 'error', message: 'Error uploading document. Please try again.' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="uploader-container">
      <div className="uploader-section">
        <h2>Upload Study Materials</h2>
        <p className="uploader-description">
          Upload PDFs or images of your study materials. These will be used as sources when answering your questions.
        </p>
        
        <form onSubmit={handleSubmit} className="upload-form">
          <div className="file-input-container">
            <input
              type="file"
              id="document-upload"
              onChange={handleFileChange}
              accept=".pdf,.jpg,.jpeg,.png"
              disabled={uploading}
              className="file-input"
            />
            <label htmlFor="document-upload" className="file-input-label">
              {file ? file.name : "Choose a file"}
            </label>
          </div>
          
          {file && (
            <div className="file-details">
              <p><strong>Name:</strong> {file.name}</p>
              <p><strong>Size:</strong> {(file.size / 1024).toFixed(2)} KB</p>
              <p><strong>Type:</strong> {file.type}</p>
            </div>
          )}
          
          <button 
            type="submit" 
            className="upload-button" 
            disabled={!file || uploading}
          >
            {uploading ? 'Processing...' : 'Upload Document'}
          </button>
        </form>
        
        {status && (
          <div className={`status-message ${status.type}`}>
            {status.message}
          </div>
        )}
      </div>
      
      <div className="uploaded-files-section">
        <h3>Uploaded Documents</h3>
        {uploadedFiles.length === 0 ? (
          <p>No documents have been uploaded yet.</p>
        ) : (
          <ul className="uploaded-files-list">
            {uploadedFiles.map((file, index) => (
              <li key={index} className="uploaded-file-item">
                <span className="file-name">{file.name}</span>
                <div className="file-info">
                  <span className="file-chunks">{file.chunks} chunks</span>
                  <span className="file-timestamp">
                    {file.timestamp.toLocaleString()}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default DocumentUploader;