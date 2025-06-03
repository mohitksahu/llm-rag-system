import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-toastify';
import { uploadDocument } from '../services/api';
import '../styles/DocumentUploader.css';

const DocumentUploader = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  
  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0]; // Handle one file at a time
    
    if (!file) return;
    
    const allowedTypes = [
      'application/pdf', 
      'image/jpeg', 
      'image/png', 
      'image/jpg'
    ];
    
    if (!allowedTypes.includes(file.type)) {
      toast.error('Only PDF and image files (JPG, PNG) are supported');
      return;
    }
    
    if (file.size > 50 * 1024 * 1024) {
      toast.error('File size must be less than 50MB');
      return;
    }
    
    setIsUploading(true);
    
    try {
      const result = await uploadDocument(file);
      
      setUploadedFiles((prev) => [
        ...prev,
        {
          name: file.name,
          uploadedAt: new Date().toISOString(),
          type: file.type,
          chunks: result.chunks_processed
        }
      ]);
      
      toast.success(`Successfully processed ${file.name} (${result.chunks_processed} chunks extracted)`);
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(`Failed to process ${file.name}. ${error.message || 'Please try again.'}`);
    } finally {
      setIsUploading(false);
    }
  };
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    disabled: isUploading,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxFiles: 1
  });

  return (
    <div className="document-uploader">
      <h2>Upload Documents</h2>
      
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''} ${isUploading ? 'uploading' : ''}`}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <div className="uploading-indicator">
            <div className="spinner"></div>
            <p>Processing document...</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📄</div>
            <p>
              {isDragActive
                ? "Drop the file here..."
                : "Drag & drop a PDF or image file, or click to select"}
            </p>
            <p className="file-hint">Supported: PDF, JPG, PNG (max 50MB)</p>
          </>
        )}
      </div>
      
      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <h3>Processed Documents</h3>
          <ul>
            {uploadedFiles.map((file, index) => (
              <li key={index} className="file-item">
                <div className="file-icon">
                  {file.type.includes('pdf') ? '📄' : '🖼️'}
                </div>
                <div className="file-details">
                  <div className="file-name">{file.name}</div>
                  <div className="file-meta">
                    {file.chunks} chunks • {new Date(file.uploadedAt).toLocaleString()}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DocumentUploader;