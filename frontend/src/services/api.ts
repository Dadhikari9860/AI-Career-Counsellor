import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add token to every request
api.interceptors.request.use(
  (config) => {
    // Always read from localStorage to get the latest token
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      // Remove authorization header if no token
      delete config.headers.Authorization;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Only redirect on 401 (unauthorized), NOT on 422 (validation errors)
    // 422 errors should be handled by the component that made the request
    if (error.response?.status === 401) {
      // Token expired or invalid - clear token and redirect
      localStorage.removeItem("token");
      // Only redirect if not already on login/register page
      const currentPath = window.location.pathname;
      if (currentPath !== "/login" && currentPath !== "/register") {
        window.location.href = "/login";
      }
    }
    // For 422 and other errors, just reject the promise
    // Components will handle the error display
    return Promise.reject(error);
  }
);

export default api;
