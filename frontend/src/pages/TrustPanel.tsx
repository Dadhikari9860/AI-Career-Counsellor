import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import "../App.css";

interface TrustPanelData {
  target_role: any;
  top_influencing_factors: Array<{
    factor: string;
    importance: number;
    user_has: boolean;
  }>;
  skill_analysis: {
    matching_skills: string[];
    missing_skills: string[];
    match_percentage: number;
  };
  recommendation_score: number;
}

const TrustPanel: React.FC = () => {
  const { user } = useAuth();
  const [data, setData] = useState<TrustPanelData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user?.target_role) {
      fetchTrustPanel();
    }
  }, [user]);

  const fetchTrustPanel = async () => {
    setLoading(true);
    try {
      const response = await api.get("/trust-panel", {
        params: { target_role: user?.target_role },
      });
      setData(response.data);
    } catch (error: any) {
      console.error("Failed to fetch trust panel:", error);
      if (error.response?.data?.suggestions) {
        setData(null);
        alert(
          `Role "${
            user?.target_role
          }" not found. Available roles: ${error.response.data.suggestions.join(
            ", "
          )}`
        );
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading trust panel...</div>;
  }

  if (!data) {
    return (
      <div className="container">
        <div className="card">
          <h2>Trust & Transparency Panel</h2>
          <p>
            Please set a target role in your profile to see recommendation
            explanations.
          </p>
        </div>
      </div>
    );
  }

  const factorData = data.top_influencing_factors.map((f) => ({
    name: f.factor,
    importance: f.importance,
    has: f.user_has ? 1 : 0,
  }));

  return (
    <div className="container">
      <div className="card">
        <h2>Why am I seeing this recommendation?</h2>
        <p>
          This panel explains how our AI system makes recommendations for you.
        </p>

        <div style={{ marginTop: "2rem" }}>
          <h3>Target Role: {data.target_role.title}</h3>
          <p>
            <strong>Recommendation Score:</strong>{" "}
            {Math.round(data.recommendation_score * 100)}%
          </p>
        </div>

        <div style={{ marginTop: "2rem" }}>
          <h3>Top Influencing Factors</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={factorData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="importance" fill="#8884d8" name="Importance %" />
            </BarChart>
          </ResponsiveContainer>

          <div style={{ marginTop: "1rem" }}>
            {data.top_influencing_factors.map((factor, index) => (
              <div
                key={index}
                style={{
                  padding: "0.75rem",
                  marginBottom: "0.5rem",
                  background: factor.user_has ? "#d4edda" : "#f8d7da",
                  borderRadius: "4px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span>
                  <strong>{factor.factor}</strong> - {factor.importance}%
                  importance
                </span>
                <span
                  style={{ color: factor.user_has ? "#28a745" : "#dc3545" }}
                >
                  {factor.user_has ? "✓ You have this" : "✗ Missing"}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ marginTop: "2rem" }}>
          <h3>Skill Analysis</h3>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1rem",
            }}
          >
            <div
              style={{
                padding: "1rem",
                background: "#d4edda",
                borderRadius: "4px",
              }}
            >
              <h4>Matching Skills ({data.skill_analysis.match_percentage}%)</h4>
              <ul style={{ marginTop: "0.5rem", paddingLeft: "1.5rem" }}>
                {data.skill_analysis.matching_skills.length > 0 ? (
                  data.skill_analysis.matching_skills.map((skill, i) => (
                    <li key={i}>{skill}</li>
                  ))
                ) : (
                  <li>None</li>
                )}
              </ul>
            </div>
            <div
              style={{
                padding: "1rem",
                background: "#f8d7da",
                borderRadius: "4px",
              }}
            >
              <h4>Missing Skills</h4>
              <ul style={{ marginTop: "0.5rem", paddingLeft: "1.5rem" }}>
                {data.skill_analysis.missing_skills.length > 0 ? (
                  data.skill_analysis.missing_skills
                    .slice(0, 10)
                    .map((skill, i) => <li key={i}>{skill}</li>)
                ) : (
                  <li>None - You have all required skills!</li>
                )}
              </ul>
            </div>
          </div>
        </div>

        <div
          style={{
            marginTop: "2rem",
            padding: "1rem",
            background: "#e7f3ff",
            borderRadius: "4px",
          }}
        >
          <h4>How Recommendations Work</h4>
          <p>Our system uses a hybrid approach combining:</p>
          <ul style={{ marginTop: "0.5rem", paddingLeft: "1.5rem" }}>
            <li>
              <strong>Content-based filtering:</strong> Matches your skills and
              experience with role requirements
            </li>
            <li>
              <strong>Collaborative filtering:</strong> Learns from similar
              users' preferences
            </li>
            <li>
              <strong>Machine learning classifier:</strong> Predicts role
              suitability based on patterns
            </li>
          </ul>
          <p style={{ marginTop: "1rem" }}>
            The recommendation score is calculated by combining these methods,
            weighted by their confidence levels.
          </p>
        </div>
      </div>
    </div>
  );
};

export default TrustPanel;
