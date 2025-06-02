import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || ''; // Will use the proxy in package.json if empty

// Send a query to the RAG system
export const sendQuery = async (query) => {
    try {
        const response = await axios.post(`${API_URL}/api/query`, { query });
        return response.data;
    } catch (error) {
        console.error('Error sending query:', error);
        throw error;
    }
};

// Upload a document to the RAG system
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
        console.error('Error uploading document:', error);
        throw error;
    }
};