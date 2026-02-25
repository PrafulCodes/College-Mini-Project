import axios from 'axios'


// API base URL - configurable via env or fallback
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/';


const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});


// Function to send financial input to backend
export const analyzeFinancialSituation = async (input) => {
  try {
    const response = await apiClient.post('/analyze', input);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

export default apiClient
