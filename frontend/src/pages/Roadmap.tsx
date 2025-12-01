import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import "../App.css";

interface RoadmapWeek {
  week: number;
  topics: string[];
  hours: number;
  focus?: string;
}

interface ProgressionLevel {
  level: string;
  title: string;
  description: string;
  weeks: RoadmapWeek[];
  total_hours: number;
  icon: string;
}

interface Roadmap {
  skill: string;
  weeks: RoadmapWeek[];
  total_weeks: number;
  estimated_total_hours: number;
  prerequisites?: {
    required: string[];
    has: string[];
    missing: string[];
    ready: boolean;
  };
  progression_levels?: ProgressionLevel[];
}

const Roadmap: React.FC = () => {
  const { user } = useAuth();
  const [searchSkill, setSearchSkill] = useState("");
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedLevel, setSelectedLevel] = useState<string | null>(null);

  // Popular skills suggestions
  const popularSkills = [
    "React",
    "Python",
    "JavaScript",
    "Node.js",
    "Database",
    "Machine Learning",
    "Docker",
    "AWS",
    "SQL",
    "Java",
    "Angular",
    "Vue.js",
    "Data Science",
    "DevOps",
  ];

  const handleSearch = async (skill?: string) => {
    const skillToSearch = skill || searchSkill.trim();
    if (!skillToSearch) {
      setError("Please enter a skill to search");
      return;
    }

    setLoading(true);
    setError("");
    setSelectedLevel(null);

    try {
      const response = await api.get("/roadmap", {
        params: { skill: skillToSearch },
      });
      setRoadmap(response.data);
    } catch (err: any) {
      setError(
        err.response?.data?.error || "Failed to load roadmap. Please try again."
      );
      setRoadmap(null);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="container" style={{ animation: "fadeIn 0.5s ease" }}>
      {/* Header */}
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
            🗺️ Learning Roadmap
          </h1>
          <p style={{ fontSize: "1.1rem", opacity: 0.95 }}>
            Search for any skill or technology to get a complete
            beginner-to-advanced learning path
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

      {/* Search Section */}
      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2 style={{ marginBottom: "1rem" }}>Search for a Skill</h2>
        <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
          <input
            type="text"
            value={searchSkill}
            onChange={(e) => setSearchSkill(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="e.g., React, Python, Database, Machine Learning..."
            style={{
              flex: 1,
              padding: "1rem",
              fontSize: "1rem",
              border: "2px solid var(--gray-300)",
              borderRadius: "var(--radius-md)",
              outline: "none",
              transition: "all 0.3s ease",
            }}
            onFocus={(e) => {
              e.currentTarget.style.borderColor = "var(--primary)";
              e.currentTarget.style.boxShadow =
                "0 0 0 3px rgba(102, 126, 234, 0.1)";
            }}
            onBlur={(e) => {
              e.currentTarget.style.borderColor = "var(--gray-300)";
              e.currentTarget.style.boxShadow = "none";
            }}
          />
          <button
            onClick={() => handleSearch()}
            disabled={loading}
            className="btn btn-primary"
            style={{
              padding: "1rem 2rem",
              fontSize: "1rem",
              fontWeight: 600,
              minWidth: "150px",
              opacity: loading ? 0.6 : 1,
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Searching..." : "🔍 Search Roadmap"}
          </button>
        </div>

        {/* Popular Skills */}
        <div>
          <p
            style={{
              marginBottom: "0.75rem",
              color: "var(--gray-600)",
              fontSize: "0.9rem",
            }}
          >
            Popular Skills:
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
            {popularSkills.map((skill) => (
              <button
                key={skill}
                onClick={() => {
                  setSearchSkill(skill);
                  handleSearch(skill);
                }}
                style={{
                  padding: "0.5rem 1rem",
                  background: "rgba(102, 126, 234, 0.1)",
                  border: "1px solid rgba(102, 126, 234, 0.2)",
                  borderRadius: "var(--radius-full)",
                  color: "var(--primary)",
                  fontSize: "0.875rem",
                  fontWeight: 500,
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "rgba(102, 126, 234, 0.2)";
                  e.currentTarget.style.transform = "translateY(-2px)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "rgba(102, 126, 234, 0.1)";
                  e.currentTarget.style.transform = "translateY(0)";
                }}
              >
                {skill}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div
          style={{
            padding: "1rem",
            marginBottom: "1rem",
            background: "#f8d7da",
            color: "#721c24",
            borderRadius: "var(--radius-md)",
            border: "1px solid #f5c6cb",
          }}
        >
          {error}
        </div>
      )}

      {/* Roadmap Display */}
      {roadmap && (
        <div style={{ animation: "slideUp 0.5s ease" }}>
          {/* Roadmap Header */}
          <div
            className="card"
            style={{
              marginBottom: "2rem",
              background:
                "linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)",
              border: "2px solid rgba(102, 126, 234, 0.2)",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                flexWrap: "wrap",
                gap: "1rem",
              }}
            >
              <div>
                <h2
                  style={{
                    margin: 0,
                    color: "var(--primary)",
                    fontSize: "2rem",
                  }}
                >
                  {roadmap.skill} Roadmap
                </h2>
                <p style={{ margin: "0.5rem 0 0 0", color: "var(--gray-600)" }}>
                  Complete learning path from beginner to advanced
                </p>
              </div>
              <div style={{ textAlign: "right" }}>
                <div
                  style={{
                    fontSize: "1.5rem",
                    fontWeight: 700,
                    color: "var(--primary)",
                  }}
                >
                  {roadmap.total_weeks} Weeks
                </div>
                <div style={{ fontSize: "0.9rem", color: "var(--gray-600)" }}>
                  {roadmap.estimated_total_hours} Hours
                </div>
              </div>
            </div>

            {/* Prerequisites */}
            {roadmap.prerequisites &&
              roadmap.prerequisites.missing &&
              roadmap.prerequisites.missing.length > 0 && (
                <div
                  style={{
                    marginTop: "1.5rem",
                    padding: "1rem",
                    background: "rgba(245, 158, 11, 0.1)",
                    borderRadius: "var(--radius-md)",
                    border: "1px solid rgba(245, 158, 11, 0.2)",
                  }}
                >
                  <div
                    style={{
                      fontSize: "0.95rem",
                      fontWeight: 600,
                      marginBottom: "0.5rem",
                      color: "var(--warning)",
                    }}
                  >
                    ⚠️ Prerequisites to Learn First:
                  </div>
                  <div style={{ fontSize: "0.9rem", color: "var(--gray-700)" }}>
                    {roadmap.prerequisites.missing.join(", ")}
                  </div>
                </div>
              )}
          </div>

          {/* Progression Levels (Beginner, Intermediate, Advanced) */}
          {roadmap.progression_levels &&
          roadmap.progression_levels.length > 0 ? (
            <div
              style={{ display: "flex", flexDirection: "column", gap: "2rem" }}
            >
              {roadmap.progression_levels.map((level, levelIdx) => (
                <div
                  key={level.level}
                  style={{
                    animation: `fadeIn 0.5s ease ${levelIdx * 0.2}s both`,
                  }}
                >
                  {/* Level Header */}
                  <div
                    className="card"
                    style={{
                      background:
                        level.level === "beginner"
                          ? "linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(22, 163, 74, 0.1) 100%)"
                          : level.level === "intermediate"
                          ? "linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%)"
                          : "linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%)",
                      border: `2px solid ${
                        level.level === "beginner"
                          ? "rgba(34, 197, 94, 0.3)"
                          : level.level === "intermediate"
                          ? "rgba(59, 130, 246, 0.3)"
                          : "rgba(168, 85, 247, 0.3)"
                      }`,
                      cursor: "pointer",
                      transition: "all 0.3s ease",
                    }}
                    onClick={() =>
                      setSelectedLevel(
                        selectedLevel === level.level ? null : level.level
                      )
                    }
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = "translateY(-4px)";
                      e.currentTarget.style.boxShadow = "var(--shadow-lg)";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = "translateY(0)";
                      e.currentTarget.style.boxShadow = "var(--shadow)";
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        flexWrap: "wrap",
                        gap: "1rem",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "1rem",
                        }}
                      >
                        <div style={{ fontSize: "3rem" }}>{level.icon}</div>
                        <div>
                          <h3
                            style={{
                              margin: 0,
                              fontSize: "1.5rem",
                              color: "var(--gray-900)",
                            }}
                          >
                            {level.title} Level
                          </h3>
                          <p
                            style={{
                              margin: "0.25rem 0 0 0",
                              color: "var(--gray-600)",
                              fontSize: "0.9rem",
                            }}
                          >
                            {level.description}
                          </p>
                        </div>
                      </div>
                      <div style={{ textAlign: "right" }}>
                        <div
                          style={{
                            fontSize: "1.25rem",
                            fontWeight: 700,
                            color: "var(--primary)",
                          }}
                        >
                          {level.weeks.length} Weeks
                        </div>
                        <div
                          style={{
                            fontSize: "0.9rem",
                            color: "var(--gray-600)",
                          }}
                        >
                          {level.total_hours} Hours
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Weeks for this level */}
                  {selectedLevel === level.level && (
                    <div
                      style={{
                        marginTop: "1rem",
                        display: "grid",
                        gridTemplateColumns:
                          "repeat(auto-fill, minmax(300px, 1fr))",
                        gap: "1rem",
                        animation: "slideDown 0.3s ease",
                      }}
                    >
                      {level.weeks.map((week, weekIdx) => (
                        <div
                          key={weekIdx}
                          className="card hover-lift"
                          style={{
                            animation: `fadeIn 0.4s ease ${
                              weekIdx * 0.1
                            }s both`,
                            border: "1px solid rgba(102, 126, 234, 0.1)",
                            transition: "all 0.3s ease",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
                              marginBottom: "0.75rem",
                            }}
                          >
                            <div>
                              <strong
                                style={{
                                  fontSize: "1.1rem",
                                  color: "var(--primary)",
                                }}
                              >
                                Week {week.week}
                              </strong>
                              {week.focus && (
                                <div
                                  style={{
                                    fontSize: "0.85rem",
                                    color: "var(--gray-600)",
                                    marginTop: "0.25rem",
                                  }}
                                >
                                  {week.focus}
                                </div>
                              )}
                            </div>
                            <div
                              style={{
                                fontSize: "0.85rem",
                                color: "var(--gray-600)",
                                fontWeight: 600,
                              }}
                            >
                              {week.hours}h
                            </div>
                          </div>
                          <div>
                            <div
                              style={{
                                fontSize: "0.9rem",
                                fontWeight: 600,
                                marginBottom: "0.5rem",
                                color: "var(--gray-700)",
                              }}
                            >
                              Topics:
                            </div>
                            <ul
                              style={{
                                margin: 0,
                                paddingLeft: "1.25rem",
                                color: "var(--gray-700)",
                                fontSize: "0.875rem",
                              }}
                            >
                              {week.topics.map((topic, topicIdx) => (
                                <li
                                  key={topicIdx}
                                  style={{ marginBottom: "0.25rem" }}
                                >
                                  {topic}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            /* Fallback: Show all weeks if progression levels not available */
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
                gap: "1rem",
              }}
            >
              {roadmap.weeks.map((week, weekIdx) => (
                <div
                  key={weekIdx}
                  className="card hover-lift"
                  style={{
                    animation: `fadeIn 0.4s ease ${weekIdx * 0.1}s both`,
                    border: "1px solid rgba(102, 126, 234, 0.1)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      marginBottom: "0.75rem",
                    }}
                  >
                    <div>
                      <strong
                        style={{ fontSize: "1.1rem", color: "var(--primary)" }}
                      >
                        Week {week.week}
                      </strong>
                      {week.focus && (
                        <div
                          style={{
                            fontSize: "0.85rem",
                            color: "var(--gray-600)",
                            marginTop: "0.25rem",
                          }}
                        >
                          {week.focus}
                        </div>
                      )}
                    </div>
                    <div
                      style={{
                        fontSize: "0.85rem",
                        color: "var(--gray-600)",
                        fontWeight: 600,
                      }}
                    >
                      {week.hours}h
                    </div>
                  </div>
                  <div>
                    <div
                      style={{
                        fontSize: "0.9rem",
                        fontWeight: 600,
                        marginBottom: "0.5rem",
                        color: "var(--gray-700)",
                      }}
                    >
                      Topics:
                    </div>
                    <ul
                      style={{
                        margin: 0,
                        paddingLeft: "1.25rem",
                        color: "var(--gray-700)",
                        fontSize: "0.875rem",
                      }}
                    >
                      {week.topics.map((topic, topicIdx) => (
                        <li key={topicIdx} style={{ marginBottom: "0.25rem" }}>
                          {topic}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!roadmap && !loading && (
        <div className="card" style={{ textAlign: "center", padding: "3rem" }}>
          <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>🗺️</div>
          <h3 style={{ color: "var(--gray-700)", marginBottom: "0.5rem" }}>
            Search for a Skill
          </h3>
          <p style={{ color: "var(--gray-600)" }}>
            Enter a skill or technology above to get a complete learning roadmap
            from beginner to advanced
          </p>
        </div>
      )}
    </div>
  );
};

export default Roadmap;
