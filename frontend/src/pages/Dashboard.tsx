import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
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

interface Recommendation {
  roles: any[];
  jobs: any[];
  resources: any[];
}

interface SkillGap {
  matching_skills: string[];
  missing_skills: string[];
  gap_percentage: number;
  match_percentage: number;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [recommendations, setRecommendations] = useState<Recommendation | null>(
    null
  );
  const [skillGap, setSkillGap] = useState<SkillGap | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [recResponse, gapResponse] = await Promise.all([
        api.get("/recommendations"),
        user?.target_role
          ? api
              .get("/skill-gap", { params: { target_role: user.target_role } })
              .catch((err) => {
                // If skill gap fails, just log it and continue
                if (err.response?.data?.suggestions) {
                  console.log(
                    "Available roles:",
                    err.response.data.suggestions
                  );
                }
                return null;
              })
          : Promise.resolve(null),
      ]);

      setRecommendations(recResponse.data);
      if (gapResponse && gapResponse.data) {
        setSkillGap(gapResponse.data.skill_gap);
      }
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (
    itemType: string,
    itemId: number,
    rating: number
  ) => {
    try {
      await api.post("/feedback", {
        item_type: itemType,
        item_id: itemId,
        rating: rating,
        feedback_type: "like",
      });
    } catch (error) {
      console.error("Failed to submit feedback:", error);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const skillGapData = skillGap
    ? [
        { skill: "Matching", value: skillGap.match_percentage },
        { skill: "Missing", value: skillGap.gap_percentage },
      ]
    : [];

  const roleScores =
    recommendations?.roles.slice(0, 5).map((r) => ({
      name: r.title,
      score: Math.round((r.score || 0) * 100),
    })) || [];

  return (
    <div className="container" style={{ animation: "fadeIn 0.5s ease" }}>
      <div
        style={{
          marginBottom: "2rem",
          padding: "2rem",
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          borderRadius: "var(--radius-xl)",
          color: "white",
          boxShadow: "var(--shadow-xl)",
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div style={{ position: "relative", zIndex: 1 }}>
          <h1
            style={{
              fontSize: "2.5rem",
              fontWeight: 700,
              marginBottom: "0.5rem",
              textShadow: "0 2px 10px rgba(0,0,0,0.2)",
            }}
          >
            Welcome back, {user?.full_name || user?.username}! 👋
          </h1>
          <p style={{ fontSize: "1.1rem", opacity: 0.95 }}>
            {user?.target_role
              ? `Ready to achieve your goal as a ${user.target_role}?`
              : "Set your target role to get personalized recommendations"}
          </p>
        </div>
        <div
          style={{
            position: "absolute",
            top: -50,
            right: -50,
            width: 200,
            height: 200,
            background: "rgba(255,255,255,0.1)",
            borderRadius: "50%",
            filter: "blur(40px)",
          }}
        ></div>
      </div>

      {!user?.target_role && (
        <div
          className="card"
          style={{
            background: "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)",
            border: "2px solid #f59e0b",
            animation: "slideUp 0.5s ease",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
            <span style={{ fontSize: "2rem" }}>⚠️</span>
            <div>
              <p
                style={{
                  fontWeight: 600,
                  marginBottom: "0.5rem",
                  color: "#92400e",
                }}
              >
                Set Your Target Role
              </p>
              <p style={{ color: "#78350f" }}>
                Please set your target role in your profile to get personalized
                recommendations.
              </p>
            </div>
          </div>
        </div>
      )}

      {skillGap && (
        <div className="card" style={{ animation: "slideUp 0.6s ease" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "1rem",
              marginBottom: "1.5rem",
            }}
          >
            <div
              style={{
                width: "50px",
                height: "50px",
                borderRadius: "var(--radius-md)",
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "1.5rem",
                boxShadow: "0 4px 15px rgba(102, 126, 234, 0.4)",
              }}
            >
              📊
            </div>
            <h2 style={{ margin: 0 }}>Skill Gap Analysis</h2>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={skillGapData}>
              <PolarGrid stroke="#e5e7eb" />
              <PolarAngleAxis
                dataKey="skill"
                tick={{ fill: "#6b7280", fontSize: 12, fontWeight: 600 }}
              />
              <PolarRadiusAxis
                angle={90}
                domain={[0, 100]}
                tick={{ fill: "#9ca3af", fontSize: 10 }}
              />
              <Radar
                name="Skills"
                dataKey="value"
                stroke="url(#colorGradient)"
                fill="url(#colorGradient)"
                fillOpacity={0.6}
                strokeWidth={2}
              />
              <defs>
                <linearGradient id="colorGradient" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#667eea" />
                  <stop offset="100%" stopColor="#764ba2" />
                </linearGradient>
              </defs>
            </RadarChart>
          </ResponsiveContainer>
          <div
            style={{
              marginTop: "2rem",
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: "1rem",
            }}
          >
            <div
              style={{
                padding: "1rem",
                background:
                  "linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%)",
                borderRadius: "var(--radius-md)",
                border: "2px solid rgba(16, 185, 129, 0.2)",
              }}
            >
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "var(--gray-600)",
                  marginBottom: "0.5rem",
                }}
              >
                Match
              </div>
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  color: "var(--success)",
                }}
              >
                {skillGap.match_percentage}%
              </div>
            </div>
            <div
              style={{
                padding: "1rem",
                background:
                  "linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%)",
                borderRadius: "var(--radius-md)",
                border: "2px solid rgba(239, 68, 68, 0.2)",
              }}
            >
              <div
                style={{
                  fontSize: "0.875rem",
                  color: "var(--gray-600)",
                  marginBottom: "0.5rem",
                }}
              >
                Gap
              </div>
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  color: "var(--danger)",
                }}
              >
                {skillGap.gap_percentage}%
              </div>
            </div>
          </div>
          <div
            style={{
              marginTop: "1.5rem",
              display: "flex",
              flexDirection: "column",
              gap: "1rem",
            }}
          >
            <div>
              <strong style={{ color: "var(--success)", fontSize: "0.9rem" }}>
                ✓ Matching Skills:
              </strong>
              <div
                style={{
                  marginTop: "0.5rem",
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "0.5rem",
                }}
              >
                {skillGap.matching_skills.length > 0 ? (
                  skillGap.matching_skills.map((skill, idx) => (
                    <span
                      key={idx}
                      className="skill-tag"
                      style={{
                        background:
                          "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                      }}
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <span
                    style={{ color: "var(--gray-500)", fontStyle: "italic" }}
                  >
                    None
                  </span>
                )}
              </div>
            </div>
            <div>
              <strong style={{ color: "var(--danger)", fontSize: "0.9rem" }}>
                ⚠ Missing Skills:
              </strong>
              <div
                style={{
                  marginTop: "0.5rem",
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "0.5rem",
                }}
              >
                {skillGap.missing_skills.slice(0, 10).map((skill, idx) => (
                  <span
                    key={idx}
                    className="skill-tag"
                    style={{
                      background:
                        "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                    }}
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="card" style={{ animation: "slideUp 0.7s ease" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "1rem",
            marginBottom: "1.5rem",
          }}
        >
          <div
            style={{
              width: "50px",
              height: "50px",
              borderRadius: "var(--radius-md)",
              background: "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "1.5rem",
              boxShadow: "0 4px 15px rgba(139, 92, 246, 0.4)",
            }}
          >
            🎯
          </div>
          <h2 style={{ margin: 0 }}>Recommended Career Roles</h2>
        </div>
        {roleScores.length > 0 && (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={roleScores}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="score" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        )}
        <div
          style={{
            marginTop: "1.5rem",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
            gap: "1.5rem",
          }}
        >
          {recommendations?.roles.slice(0, 5).map((role, idx) => (
            <div
              key={role.id}
              className="hover-lift"
              style={{
                padding: "1.5rem",
                background:
                  "linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%)",
                borderRadius: "var(--radius-lg)",
                border: "2px solid rgba(139, 92, 246, 0.2)",
                position: "relative",
                overflow: "hidden",
                animation: `slideUp ${0.8 + idx * 0.1}s ease`,
              }}
            >
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  right: 0,
                  width: "100px",
                  height: "100px",
                  background:
                    "linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%)",
                  borderRadius: "50%",
                  transform: "translate(30%, -30%)",
                  filter: "blur(20px)",
                }}
              ></div>
              <div style={{ position: "relative", zIndex: 1 }}>
                <h3
                  style={{
                    marginTop: 0,
                    marginBottom: "0.75rem",
                    fontSize: "1.25rem",
                    fontWeight: 700,
                    color: "var(--gray-900)",
                  }}
                >
                  {role.title}
                </h3>
                {role.description && (
                  <p
                    style={{
                      color: "#6b7280",
                      margin: "0.75rem 0",
                      fontSize: "0.9rem",
                      lineHeight: "1.6",
                    }}
                  >
                    {role.description?.substring(0, 120)}...
                  </p>
                )}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "0.5rem",
                    margin: "1rem 0",
                    padding: "0.75rem",
                    background: "white",
                    borderRadius: "var(--radius-md)",
                    boxShadow: "var(--shadow-sm)",
                  }}
                >
                  <span style={{ fontSize: "1.5rem" }}>📊</span>
                  <div>
                    <div
                      style={{
                        fontSize: "0.75rem",
                        color: "var(--gray-500)",
                        textTransform: "uppercase",
                        letterSpacing: "0.5px",
                      }}
                    >
                      Match Score
                    </div>
                    <div
                      style={{
                        fontSize: "1.5rem",
                        fontWeight: 700,
                        background:
                          "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)",
                        WebkitBackgroundClip: "text",
                        WebkitTextFillColor: "transparent",
                        backgroundClip: "text",
                      }}
                    >
                      {Math.round((role.score || 0) * 100)}%
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleFeedback("role", role.id, 5)}
                  className="btn btn-primary"
                  style={{
                    width: "100%",
                    marginTop: "0.5rem",
                    fontSize: "0.9rem",
                    padding: "0.75rem",
                  }}
                >
                  👍 Like This Role
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card" style={{ animation: "slideUp 0.8s ease" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "1rem",
            marginBottom: "1.5rem",
          }}
        >
          <div
            style={{
              width: "50px",
              height: "50px",
              borderRadius: "var(--radius-md)",
              background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "1.5rem",
              boxShadow: "0 4px 15px rgba(16, 185, 129, 0.4)",
            }}
          >
            💼
          </div>
          <h2 style={{ margin: 0 }}>Recommended Jobs</h2>
          {user?.location && (
            <p
              style={{
                margin: "0.5rem 0 0 0",
                fontSize: "0.875rem",
                color: "var(--gray-600)",
                fontStyle: "italic",
              }}
            >
              Filtered by your location: {user.location}
            </p>
          )}
        </div>
        {recommendations?.jobs && recommendations.jobs.length > 0 ? (
          recommendations.jobs.slice(0, 5).map((job: any) => (
            <div
              key={job.id || job.title}
              className="hover-lift"
              style={{
                marginBottom: "1.5rem",
                padding: "1.5rem",
                background:
                  "linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(5, 150, 105, 0.05) 100%)",
                borderRadius: "var(--radius-lg)",
                border: "2px solid rgba(16, 185, 129, 0.2)",
                position: "relative",
                overflow: "hidden",
                animation: "slideUp 0.8s ease",
              }}
            >
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  right: 0,
                  width: "120px",
                  height: "120px",
                  background:
                    "linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%)",
                  borderRadius: "50%",
                  transform: "translate(30%, -30%)",
                  filter: "blur(30px)",
                }}
              ></div>
              <div style={{ position: "relative", zIndex: 1 }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "start",
                    marginBottom: "1rem",
                  }}
                >
                  <div style={{ flex: 1 }}>
                    <h3
                      style={{
                        marginTop: 0,
                        marginBottom: "0.5rem",
                        fontSize: "1.3rem",
                        fontWeight: 700,
                        color: "var(--gray-900)",
                      }}
                    >
                      {job.title}
                    </h3>
                    <p
                      style={{
                        color: "var(--primary)",
                        margin: "0.25rem 0",
                        fontWeight: 600,
                        fontSize: "1rem",
                      }}
                    >
                      {job.company}
                    </p>
                  </div>
                  {job.source && (
                    <span
                      style={{
                        display: "inline-block",
                        padding: "0.375rem 0.75rem",
                        background:
                          job.source === "linkedin"
                            ? "linear-gradient(135deg, #0077b5 0%, #005885 100%)"
                            : "var(--gray-500)",
                        color: "white",
                        borderRadius: "var(--radius-full)",
                        fontSize: "0.75rem",
                        fontWeight: 600,
                        textTransform: "uppercase",
                        letterSpacing: "0.5px",
                        boxShadow: "var(--shadow)",
                      }}
                    >
                      {job.source === "linkedin"
                        ? "🔗 LinkedIn"
                        : "📋 Generated"}
                    </span>
                  )}
                </div>
                {job.description && (
                  <p
                    style={{
                      color: "var(--gray-600)",
                      margin: "0.75rem 0",
                      lineHeight: "1.6",
                      fontSize: "0.9rem",
                    }}
                  >
                    {job.description?.substring(0, 150)}...
                  </p>
                )}
                <div
                  style={{
                    display: "flex",
                    gap: "1rem",
                    margin: "1rem 0",
                    flexWrap: "wrap",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      padding: "0.5rem 0.75rem",
                      background: "rgba(99, 102, 241, 0.1)",
                      borderRadius: "var(--radius-md)",
                    }}
                  >
                    <span>📍</span>
                    <span
                      style={{ fontSize: "0.875rem", color: "var(--gray-700)" }}
                    >
                      {job.location || "Not specified"}
                    </span>
                  </div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      padding: "0.5rem 0.75rem",
                      background:
                        (job.match_score || job.score || 0) >= 0.5
                          ? "rgba(16, 185, 129, 0.1)"
                          : (job.match_score || job.score || 0) >= 0.3
                          ? "rgba(245, 158, 11, 0.1)"
                          : "rgba(239, 68, 68, 0.1)",
                      borderRadius: "var(--radius-md)",
                    }}
                  >
                    <span>🎯</span>
                    <span
                      style={{
                        fontSize: "0.875rem",
                        fontWeight: 600,
                        color:
                          (job.match_score || job.score || 0) >= 0.5
                            ? "var(--success)"
                            : (job.match_score || job.score || 0) >= 0.3
                            ? "var(--warning)"
                            : "var(--danger)",
                      }}
                    >
                      {Math.round((job.match_score || job.score || 0.01) * 100)}
                      % Match
                    </span>
                  </div>
                </div>
                {job.matched_skills && job.matched_skills.length > 0 && (
                  <div
                    style={{
                      marginTop: "0.75rem",
                      padding: "0.75rem",
                      background: "rgba(99, 102, 241, 0.05)",
                      borderRadius: "var(--radius-md)",
                      border: "1px solid rgba(99, 102, 241, 0.1)",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "0.875rem",
                        fontWeight: 600,
                        color: "var(--gray-700)",
                        marginBottom: "0.5rem",
                      }}
                    >
                      ✨ Matched Your Skills:
                    </div>
                    <div
                      style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "0.5rem",
                      }}
                    >
                      {job.matched_skills
                        .slice(0, 8)
                        .map((skill: string, idx: number) => (
                          <span
                            key={idx}
                            style={{
                              padding: "0.25rem 0.75rem",
                              background: "rgba(99, 102, 241, 0.15)",
                              color: "var(--primary)",
                              borderRadius: "var(--radius-full)",
                              fontSize: "0.8rem",
                              fontWeight: 500,
                            }}
                          >
                            {skill}
                          </span>
                        ))}
                      {job.matched_skills.length > 8 && (
                        <span
                          style={{
                            padding: "0.25rem 0.75rem",
                            color: "var(--gray-600)",
                            fontSize: "0.8rem",
                          }}
                        >
                          +{job.matched_skills.length - 8} more
                        </span>
                      )}
                    </div>
                  </div>
                )}
                <div
                  style={{
                    marginTop: "1rem",
                    display: "flex",
                    gap: "0.75rem",
                    flexWrap: "wrap",
                  }}
                >
                  <a
                    href={
                      job.url ||
                      `https://www.linkedin.com/jobs/search?keywords=${encodeURIComponent(
                        job.title || ""
                      )}`
                    }
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      padding: "0.75rem 1.5rem",
                      background:
                        job.source === "linkedin"
                          ? "linear-gradient(135deg, #0077b5 0%, #005885 100%)"
                          : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                      color: "white",
                      textDecoration: "none",
                      borderRadius: "var(--radius-md)",
                      fontWeight: 600,
                      transition: "all 0.3s ease",
                      boxShadow: "var(--shadow)",
                      flex: 1,
                      minWidth: "200px",
                      justifyContent: "center",
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = "translateY(-2px)";
                      e.currentTarget.style.boxShadow = "var(--shadow-lg)";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = "translateY(0)";
                      e.currentTarget.style.boxShadow = "var(--shadow)";
                    }}
                  >
                    {job.source === "linkedin" ? (
                      <>🔗 View on LinkedIn →</>
                    ) : (
                      <>🔍 Search on LinkedIn →</>
                    )}
                  </a>
                  <button
                    onClick={() => handleFeedback("job", job.id, 5)}
                    className="btn btn-primary"
                    style={{
                      padding: "0.75rem 1.5rem",
                      flex: 1,
                      minWidth: "120px",
                    }}
                  >
                    👍 Like
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p>No job recommendations available.</p>
        )}
      </div>

      <div className="card" style={{ animation: "slideUp 0.9s ease" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "1rem",
            marginBottom: "1.5rem",
          }}
        >
          <div
            style={{
              width: "50px",
              height: "50px",
              borderRadius: "var(--radius-md)",
              background: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "1.5rem",
              boxShadow: "0 4px 15px rgba(245, 158, 11, 0.4)",
            }}
          >
            📚
          </div>
          <h2 style={{ margin: 0 }}>Learning Resources</h2>
        </div>
        <p style={{ color: "#666", marginBottom: "1rem" }}>
          Resources to help you learn the missing skills for your target role
        </p>
        {recommendations?.resources && recommendations.resources.length > 0 ? (
          recommendations.resources.slice(0, 8).map((resource: any) => (
            <div
              key={resource.id}
              style={{
                marginBottom: "1rem",
                padding: "1rem",
                background: "#f8f9fa",
                borderRadius: "4px",
                border: "1px solid #ddd",
                transition: "all 0.3s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = "0 2px 8px rgba(0,0,0,0.1)";
                e.currentTarget.style.transform = "translateY(-2px)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = "none";
                e.currentTarget.style.transform = "translateY(0)";
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "start",
                }}
              >
                <div style={{ flex: 1 }}>
                  <h3 style={{ marginTop: 0, marginBottom: "0.5rem" }}>
                    {resource.title}
                  </h3>
                  {resource.description && (
                    <p style={{ color: "#666", margin: "0.5rem 0" }}>
                      {resource.description}
                    </p>
                  )}
                  {resource.missing_skill && (
                    <p
                      style={{
                        margin: "0.5rem 0",
                        color: "#ff9800",
                        fontWeight: "500",
                      }}
                    >
                      <strong>Addresses skill gap:</strong>{" "}
                      {resource.missing_skill}
                    </p>
                  )}
                  <div
                    style={{
                      display: "flex",
                      gap: "1rem",
                      marginTop: "0.5rem",
                      flexWrap: "wrap",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        gap: "1rem",
                        marginTop: "0.5rem",
                        flexWrap: "wrap",
                      }}
                    >
                      {resource.provider && (
                        <span
                          style={{
                            padding: "0.25rem 0.5rem",
                            background:
                              resource.provider === "YouTube"
                                ? "#FF0000"
                                : "#6c757d",
                            color: "white",
                            borderRadius: "4px",
                            fontSize: "0.75rem",
                            fontWeight: "500",
                          }}
                        >
                          📺 {resource.provider}
                        </span>
                      )}
                      {resource.resource_type && (
                        <span style={{ color: "#666", fontSize: "0.9rem" }}>
                          <strong>Type:</strong> {resource.resource_type}
                        </span>
                      )}
                      {resource.difficulty_level && (
                        <span style={{ color: "#666", fontSize: "0.9rem" }}>
                          <strong>Level:</strong> {resource.difficulty_level}
                        </span>
                      )}
                    </div>
                    {resource.duration && (
                      <span style={{ color: "#666", fontSize: "0.9rem" }}>
                        <strong>Duration:</strong> {resource.duration}
                      </span>
                    )}
                    {resource.provider && (
                      <span
                        style={{
                          padding: "0.25rem 0.5rem",
                          background:
                            resource.provider === "YouTube"
                              ? "#FF0000"
                              : "#6c757d",
                          color: "white",
                          borderRadius: "4px",
                          fontSize: "0.75rem",
                          fontWeight: "500",
                        }}
                      >
                        📺 {resource.provider}
                      </span>
                    )}
                    {resource.difficulty_level && (
                      <span style={{ color: "#666", fontSize: "0.9rem" }}>
                        <strong>Level:</strong> {resource.difficulty_level}
                      </span>
                    )}
                  </div>
                  {resource.skills_covered &&
                    resource.skills_covered.length > 0 && (
                      <div
                        style={{
                          marginTop: "0.5rem",
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "0.25rem",
                        }}
                      >
                        {resource.skills_covered.map(
                          (skill: string, idx: number) => (
                            <span
                              key={idx}
                              style={{
                                padding: "0.25rem 0.5rem",
                                background: "#007bff",
                                color: "white",
                                borderRadius: "12px",
                                fontSize: "0.75rem",
                              }}
                            >
                              {skill}
                            </span>
                          )
                        )}
                      </div>
                    )}
                </div>
              </div>
              <a
                href={
                  resource.url ||
                  `https://www.youtube.com/results?search_query=${encodeURIComponent(
                    resource.missing_skill || resource.title || "tutorial"
                  )}`
                }
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "inline-block",
                  marginTop: "1rem",
                  padding: "0.5rem 1rem",
                  background:
                    resource.provider === "YouTube" ? "#FF0000" : "#28a745",
                  color: "white",
                  textDecoration: "none",
                  borderRadius: "4px",
                  fontWeight: "500",
                  transition: "background 0.3s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background =
                    resource.provider === "YouTube" ? "#CC0000" : "#218838";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background =
                    resource.provider === "YouTube" ? "#FF0000" : "#28a745";
                }}
              >
                {resource.provider === "YouTube"
                  ? "📺 Watch on YouTube →"
                  : "Start Learning →"}
              </a>
            </div>
          ))
        ) : (
          <p>
            No learning resources available. Update your profile to see
            recommended resources.
          </p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
