import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Chatbot from "./pages/Chatbot";
import Profile from "./pages/Profile";
import CareerPathSimulator from "./pages/CareerPathSimulator";
import TrustPanel from "./pages/TrustPanel";
import Quiz from "./pages/Quiz";
import Roadmap from "./pages/Roadmap";
import Navbar from "./components/Navbar";
import "./App.css";

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return user ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <Navbar />
                  <Dashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/chatbot"
              element={
                <PrivateRoute>
                  <Navbar />
                  <Chatbot />
                </PrivateRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <Navbar />
                  <Profile />
                </PrivateRoute>
              }
            />
            <Route
              path="/career-path"
              element={
                <PrivateRoute>
                  <Navbar />
                  <CareerPathSimulator />
                </PrivateRoute>
              }
            />
            <Route
              path="/trust-panel"
              element={
                <PrivateRoute>
                  <Navbar />
                  <TrustPanel />
                </PrivateRoute>
              }
            />
            <Route
              path="/quiz"
              element={
                <PrivateRoute>
                  <Navbar />
                  <Quiz />
                </PrivateRoute>
              }
            />
            <Route
              path="/roadmap"
              element={
                <PrivateRoute>
                  <Navbar />
                  <Roadmap />
                </PrivateRoute>
              }
            />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
