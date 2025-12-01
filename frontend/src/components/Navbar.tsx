import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import "../App.css";

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const isActive = (path: string) => location.pathname === path;

  const navLinks = [
    { path: "/dashboard", label: "Dashboard", icon: "📊" },
    { path: "/chatbot", label: "Chatbot", icon: "💬" },
    { path: "/profile", label: "Profile", icon: "👤" },
    { path: "/career-path", label: "Career Path", icon: "🎯" },
    { path: "/roadmap", label: "Roadmap", icon: "🗺️" },
    { path: "/trust-panel", label: "Trust Panel", icon: "🔒" },
    { path: "/quiz", label: "Quiz", icon: "📝" },
  ];

  return (
    <nav
      className="navbar"
      style={{
        background: "rgba(255, 255, 255, 0.95)",
        backdropFilter: "blur(10px)",
        boxShadow:
          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        padding: "1rem 2rem",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        position: "sticky",
        top: 0,
        zIndex: 1000,
        borderBottom: "1px solid rgba(0, 0, 0, 0.1)",
      }}
    >
      <div style={{ display: "flex", gap: "3rem", alignItems: "center" }}>
        <Link
          to="/dashboard"
          style={{
            color: "var(--primary)",
            textDecoration: "none",
            fontWeight: 700,
            fontSize: "1.5rem",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
          }}
        >
          <span style={{ fontSize: "1.8rem" }}>🚀</span>
          Career Guidance
        </Link>

        {/* Desktop Navigation */}
        <div
          style={{
            display: "flex",
            gap: "0.5rem",
            alignItems: "center",
          }}
        >
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              style={{
                color: isActive(link.path)
                  ? "var(--primary)"
                  : "var(--gray-700)",
                textDecoration: "none",
                padding: "0.5rem 1rem",
                borderRadius: "var(--radius-md)",
                fontWeight: isActive(link.path) ? 600 : 500,
                background: isActive(link.path)
                  ? "rgba(99, 102, 241, 0.1)"
                  : "transparent",
                transition: "all 0.3s ease",
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                borderBottom: isActive(link.path)
                  ? "2px solid var(--primary)"
                  : "2px solid transparent",
              }}
              onMouseEnter={(e) => {
                if (!isActive(link.path)) {
                  e.currentTarget.style.background = "rgba(99, 102, 241, 0.05)";
                  e.currentTarget.style.color = "var(--primary)";
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive(link.path)) {
                  e.currentTarget.style.background = "transparent";
                  e.currentTarget.style.color = "var(--gray-700)";
                }
              }}
            >
              <span>{link.icon}</span>
              {link.label}
            </Link>
          ))}
        </div>
      </div>

      <div
        style={{
          display: "flex",
          gap: "1rem",
          alignItems: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
            padding: "0.5rem 1rem",
            background: "rgba(99, 102, 241, 0.1)",
            borderRadius: "var(--radius-full)",
          }}
        >
          <div
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "white",
              fontWeight: 600,
              fontSize: "0.875rem",
            }}
          >
            {user?.username?.charAt(0).toUpperCase() || "U"}
          </div>
          <span
            style={{
              color: "var(--gray-700)",
              fontWeight: 600,
              fontSize: "0.9rem",
            }}
          >
            {user?.username}
          </span>
        </div>
        <button
          onClick={handleLogout}
          className="btn btn-secondary"
          style={{
            padding: "0.5rem 1.25rem",
            fontSize: "0.9rem",
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
