import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import api from "../services/api";

interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  location?: string;
  skills?: any[];
  experience_years?: number;
  current_role?: string;
  target_role?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (
    username: string,
    email: string,
    password: string,
    fullName?: string,
    location?: string
  ) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
  setToken: (token: string | null) => void;
  setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      // Token is already in localStorage, interceptor will pick it up
      fetchUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const response = await api.get("/me");
      setUser(response.data);
    } catch (error) {
      console.error("Failed to fetch user:", error);
      localStorage.removeItem("token");
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    const response = await api.post("/login", { username, password });
    const { access_token, user: userData } = response.data;
    // Store token first
    localStorage.setItem("token", access_token);
    setToken(access_token);
    setUser(userData);
    // Interceptor will automatically add token to subsequent requests
  };

  const register = async (
    username: string,
    email: string,
    password: string,
    fullName?: string
  ) => {
    try {
      const response = await api.post("/register", {
        username,
        email,
        password,
        full_name: fullName || "",
      });
      const { access_token, user: userData } = response.data;
      // Store token first
      localStorage.setItem("token", access_token);
      setToken(access_token);
      setUser(userData);
      // Interceptor will automatically add token to subsequent requests
    } catch (error: any) {
      console.error("Registration error:", error);
      const errorMessage =
        error.response?.data?.error || error.message || "Registration failed";
      throw new Error(errorMessage);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    // Interceptor will automatically remove token from requests
  };

  const updateUser = (userData: Partial<User>) => {
    setUser((prev) => (prev ? { ...prev, ...userData } : null));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
        updateUser,
        setToken,
        setUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
