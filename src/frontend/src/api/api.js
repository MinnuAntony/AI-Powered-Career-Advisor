
import axios from "axios";

/*
  NOTE: 
  - During local dev, we use localhost:8000 (FastAPI dev server)
  - When Dockerized / in production, change API_BASE to the backend container's hostname or public domain
*/
const API_BASE = "http://localhost:8000/api/v1";

// No more submitAssessment, we send directly to /recommend
export const submitCareerRequest = async (data) => {
  try {
    const response = await axios.post(`${API_BASE}/recommend`, data);
    return response.data;
  } catch (err) {
    console.error("Error submitting career request:", err.response?.data || err);
    throw err;
  }
};
