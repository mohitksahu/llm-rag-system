import axios from 'axios';

// Change this to the ngrok URL provided by your Google Colab notebook
// For example: https://a1b2-35-123-234-12.ngrok.io
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

console.log('Connecting to backend at:', API_URL);

// Configure axios
const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Send a query to the RAG system
 */
export const sendQuery = async (query) => {
  try {
    const response = await api.post('/query', { query });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Upload a document to the RAG system
 */
export const uploadDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_URL}/api/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('Upload Error:', error);
    throw error;
  }
};

/**
 * Check the backend server status
 */
export const checkServerStatus = async () => {
  try {
    const response = await api.get('/status');
    return response.data;
  } catch (error) {
    console.error('Status check error:', error);
    throw error;
  }
};