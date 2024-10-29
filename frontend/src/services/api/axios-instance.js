// src/services/api/axios-instance.js
import axios from "axios";
import AuthCookies from "../cookie/authToken.cookie";

const BASE_URL = import.meta.env.VITE_BASE_API_URL.endsWith('/') 
  ? import.meta.env.VITE_BASE_API_URL 
  : `${import.meta.env.VITE_BASE_API_URL}/`;

// Create an Axios instance
const axiosInstance = axios.create({
  baseURL: BASE_URL, // Ensure BASE_URL is used properly
});

// // Set up a request interceptor
// axiosInstance.interceptors.request.use(
//   (config) => {
//     const token = AuthCookies.GetAccessToken();
//     if (token) {
//       config.headers["Authorization"] = `Bearer ${token}`;
//     }
  
//     return config;
//   },
//   (error) => {
//     console.error("Request error:", error);
//     return Promise.reject(error);
//   }
// );


export default axiosInstance;
