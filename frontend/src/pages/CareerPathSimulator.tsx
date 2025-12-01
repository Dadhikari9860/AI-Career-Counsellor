import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import "../App.css";

interface CareerPath {
  target_role: any;
  current_experience: number;
  current_skill_match: number;
  career_path: Array<{
    level: string;
    years_experience_required: number;
    years_from_current: number;
    estimated_time_to_reach: string;
    required_skills: string[];
  }>;
}

const CareerPathSimulator: React.FC = () => {
  const { user } = useAuth();
  const [careerPath, setCareerPath] = useState<CareerPath | null>(null);
  const [targetRole, setTargetRole] = useState(user?.target_role || "");
  const [loading, setLoading] = useState(false);
  const [availableRoles, setAvailableRoles] = useState<string[]>([]);

  useEffect(() => {
    if (user?.target_role) {
      fetchCareerPath(user.target_role);
    }
    // Fetch available roles
    api
      .get("/roles")
      .then((response) => {
        setAvailableRoles(response.data.roles.map((r: any) => r.title));
      })
      .catch((error) => {
        console.error("Failed to fetch roles:", error);
      });
  }, [user]);

  const fetchCareerPath = async (role: string) => {
    if (!role) {
      setLoading(false);
      return;
    }
    setLoading(true);
    try {
      const response = await api.get("/career-path-simulator", {
        params: { target_role: role },
      });
      if (response.data) {
        setCareerPath(response.data);
      } else {
        throw new Error("No data received");
      }
    } catch (error: any) {
      console.error("Failed to fetch career path:", error);
      setCareerPath(null);
      if (error.response?.data?.suggestions) {
        alert(
          `Role "${role}" not found. Available roles: ${error.response.data.suggestions.join(
            ", "
          )}`
        );
      } else {
        const errorMsg =
          error.response?.data?.error ||
          error.message ||
          "Failed to fetch career path";
        console.error("Career path error:", errorMsg);
        // Don't show alert for every error, just log it
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTargetRole(e.target.value);
  };

  const handleSimulate = () => {
    if (targetRole) {
      fetchCareerPath(targetRole);
    }
  };

  if (loading) {
    return <div className="loading">Loading career path...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h2>Career Path Simulator</h2>
        <p>Select a target role to see your career progression path</p>

        <div className="form-group" style={{ marginBottom: "1rem" }}>
          <label>Target Role</label>
          <div style={{ display: "flex", gap: "0.5rem" }}>
            {availableRoles.length > 0 ? (
              <select
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                style={{ flex: 1, padding: "0.75rem" }}
              >
                <option value="">Select a role...</option>
                {availableRoles.map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={targetRole}
                onChange={handleRoleChange}
                placeholder="e.g., Full Stack Developer"
                style={{ flex: 1 }}
                list="role-suggestions"
              />
            )}
            <datalist id="role-suggestions">
              {availableRoles.map((role) => (
                <option key={role} value={role} />
              ))}
            </datalist>
            <button onClick={handleSimulate} className="btn btn-primary">
              Simulate
            </button>
          </div>
          {availableRoles.length > 0 && (
            <small
              style={{ color: "#666", marginTop: "0.25rem", display: "block" }}
            >
              Available roles: {availableRoles.join(", ")}
            </small>
          )}
        </div>

        {careerPath && (
          <div>
            <div
              style={{
                marginBottom: "2rem",
                padding: "1rem",
                background: "#e7f3ff",
                borderRadius: "4px",
              }}
            >
              <h3>Current Status</h3>
              <p>
                <strong>Target Role:</strong> {careerPath.target_role.title}
              </p>
              <p>
                <strong>Current Experience:</strong>{" "}
                {careerPath.current_experience} years
              </p>
              <p>
                <strong>Current Skill Match:</strong>{" "}
                {careerPath.current_skill_match}%
              </p>
            </div>

            <h3>Career Progression Path</h3>
            <div
              style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
            >
              {careerPath.career_path.map((step, index) => (
                <div
                  key={index}
                  style={{
                    padding: "1.5rem",
                    border: "2px solid #007bff",
                    borderRadius: "8px",
                    background: index === 0 ? "#fff3cd" : "white",
                    position: "relative",
                  }}
                >
                  {index > 0 && (
                    <div
                      style={{
                        position: "absolute",
                        left: "50%",
                        top: "-20px",
                        transform: "translateX(-50%)",
                        background: "#007bff",
                        color: "white",
                        padding: "0.25rem 0.75rem",
                        borderRadius: "4px",
                        fontSize: "0.9rem",
                      }}
                    >
                      ↓
                    </div>
                  )}
                  <h4 style={{ marginBottom: "0.5rem", color: "#007bff" }}>
                    {step.level}
                  </h4>
                  <p>
                    <strong>Years of Experience Required:</strong>{" "}
                    {step.years_experience_required} years
                  </p>
                  <p>
                    <strong>Years from Current Position:</strong>{" "}
                    {step.years_from_current} years
                  </p>
                  <p>
                    <strong>Estimated Time to Reach:</strong>{" "}
                    {step.estimated_time_to_reach}
                  </p>
                  {step.required_skills.length > 0 && (
                    <div>
                      <strong>Required Skills:</strong>
                      <ul
                        style={{ marginTop: "0.5rem", paddingLeft: "1.5rem" }}
                      >
                        {step.required_skills.map((skill, i) => (
                          <li key={i}>{skill}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {!careerPath && (
          <div style={{ textAlign: "center", padding: "2rem", color: "#666" }}>
            Enter a target role and click "Simulate" to see your career path
          </div>
        )}
      </div>
    </div>
  );
};

export default CareerPathSimulator;
