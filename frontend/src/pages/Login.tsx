import React, { useState, useEffect, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import "../App.css";

declare global {
  interface Window {
    google: any;
  }
}

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleClientId, setGoogleClientId] = useState<string | null>(null);
  const { login, setToken, setUser } = useAuth();
  const navigate = useNavigate();
  const googleButtonRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Fetch Google OAuth config
    api
      .get("/auth/google/config")
      .then((response) => {
        if (response.data.enabled && response.data.client_id) {
          setGoogleClientId(response.data.client_id);
        }
      })
      .catch((err) => {
        console.log("Google OAuth not configured:", err);
      });
  }, []);

  useEffect(() => {
    // Wait for Google script to load, then initialize
    const checkGoogleScript = () => {
      if (window.google && googleClientId && googleButtonRef.current) {
        initializeGoogleSignIn(googleClientId);
      } else if (googleClientId) {
        // Retry after a short delay if script not loaded yet
        setTimeout(checkGoogleScript, 100);
      }
    };

    checkGoogleScript();
  }, [googleClientId]);

  const initializeGoogleSignIn = (clientId: string) => {
    if (window.google && googleButtonRef.current) {
      // Clear any existing button
      googleButtonRef.current.innerHTML = "";

      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: handleGoogleSignIn,
      });

      window.google.accounts.id.renderButton(googleButtonRef.current, {
        theme: "outline",
        size: "large",
        width: "100%",
        text: "signin_with",
        locale: "en",
      });
    }
  };

  const handleGoogleSignIn = async (response: any) => {
    try {
      setError("");
      setLoading(true);

      // Verify the token with backend
      const result = await api.post("/auth/google/verify", {
        token: response.credential,
      });

      const { access_token, user: userData } = result.data;
      localStorage.setItem("token", access_token);
      setToken(access_token);
      setUser(userData);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.error || "Google login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(username, password);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.error || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Animated Background Elements */}
      <div
        style={{
          position: "absolute",
          top: "-50%",
          left: "-50%",
          width: "200%",
          height: "200%",
          background:
            "radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px)",
          backgroundSize: "50px 50px",
          animation: "pulse 20s infinite",
        }}
      ></div>

      <div
        className="card"
        style={{
          width: "450px",
          maxWidth: "90%",
          animation: "slideUp 0.5s ease",
          position: "relative",
          zIndex: 1,
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <div
            style={{
              width: "80px",
              height: "80px",
              margin: "0 auto 1rem",
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "2.5rem",
              boxShadow: "0 10px 30px rgba(102, 126, 234, 0.4)",
            }}
          >
            🚀
          </div>
          <h2
            style={{
              fontSize: "2rem",
              fontWeight: 700,
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
              marginBottom: "0.5rem",
            }}
          >
            Welcome Back
          </h2>
          <p style={{ color: "var(--gray-600)", fontSize: "0.9rem" }}>
            Sign in to continue your career journey
          </p>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error">{error}</div>}
          <button
            type="submit"
            className="btn btn-primary"
            style={{
              width: "100%",
              marginTop: "1rem",
              padding: "1rem",
              fontSize: "1.1rem",
              fontWeight: 600,
            }}
            disabled={loading}
          >
            {loading ? (
              <span
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "0.5rem",
                }}
              >
                <span
                  className="spinner"
                  style={{ width: "20px", height: "20px", borderWidth: "2px" }}
                ></span>
                Logging in...
              </span>
            ) : (
              "Login"
            )}
          </button>

          {googleClientId && (
            <div style={{ marginTop: "1.5rem", marginBottom: "1.5rem" }}>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "0.75rem",
                  marginBottom: "1rem",
                }}
              >
                <div
                  style={{
                    flex: 1,
                    height: "1px",
                    background: "var(--gray-300)",
                  }}
                ></div>
                <span
                  style={{
                    color: "var(--gray-500)",
                    fontSize: "0.875rem",
                    fontWeight: 500,
                  }}
                >
                  OR
                </span>
                <div
                  style={{
                    flex: 1,
                    height: "1px",
                    background: "var(--gray-300)",
                  }}
                ></div>
              </div>
              <div
                ref={googleButtonRef}
                style={{
                  width: "100%",
                  display: "flex",
                  justifyContent: "center",
                }}
              ></div>
            </div>
          )}

          <p
            style={{
              textAlign: "center",
              marginTop: "1.5rem",
              color: "var(--gray-600)",
            }}
          >
            Don't have an account?{" "}
            <Link
              to="/register"
              style={{
                color: "var(--primary)",
                fontWeight: 600,
                textDecoration: "none",
                borderBottom: "2px solid var(--primary)",
                transition: "all 0.3s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = "var(--primary-dark)";
                e.currentTarget.style.borderBottomColor = "var(--primary-dark)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = "var(--primary)";
                e.currentTarget.style.borderBottomColor = "var(--primary)";
              }}
            >
              Register Now
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;
