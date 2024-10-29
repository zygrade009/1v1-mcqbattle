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

// Set up a request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = AuthCookies.GetAccessToken();
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
  
    return config;
  },
  (error) => {
    console.error("Request error:", error);
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    console.error("Response error:", error.response);

    if (error.response && error.response.status === 401&&!originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = AuthCookies.GetRefreshToken();
        if (!refreshToken) {
          console.error("No refresh token available");
          AuthCookies.ClearAll();
          window.location.href = '/login';
          return Promise.reject(error);
        }

        const refreshResponse = await axios.post(`${BASE_URL}api/token/refresh/`, {
          refresh: refreshToken
        });

        const { access } = refreshResponse.data;
        AuthCookies.SetAccessToken(access);

        originalRequest.headers["Authorization"] = `Bearer ${access}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        AuthCookies.ClearAll();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
