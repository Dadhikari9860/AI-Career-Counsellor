import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import "../App.css";

interface Message {
  id: string;
  text: string;
  sender: "user" | "assistant";
  timestamp: Date;
  data?: any;
  suggestions?: string[];
}

const Chatbot: React.FC = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: `Hello ${
        user?.full_name || user?.username || "there"
      }! 👋 I'm your career guidance assistant. I can help you with:\n• Career recommendations\n• Job search\n• Skill gap analysis\n• Learning paths\n• Resume tips\n\nWhat would you like to explore today?`,
      sender: "assistant",
      timestamp: new Date(),
      suggestions: [
        "Get career recommendations",
        "Find jobs",
        "Analyze my skills",
        "Show learning resources",
      ],
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await api.post("/chat", { message: input });
      const data = response.data;

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.message || "I'm here to help!",
        sender: "assistant",
        timestamp: new Date(),
        data: data.data,
        suggestions: data.suggestions || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error. Please try again.",
        sender: "assistant",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    // Auto-send after a brief delay
    setTimeout(() => {
      handleSend();
    }, 100);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const renderMessageContent = (message: Message) => {
    // Render text with line breaks
    const textLines = message.text.split("\n");

    return (
      <div>
        {textLines.map((line, idx) => (
          <div
            key={idx}
            style={{ marginBottom: idx < textLines.length - 1 ? "0.5rem" : 0 }}
          >
            {line}
          </div>
        ))}

        {/* Render data if available */}
        {message.data?.recommended_roles && (
          <div style={{ marginTop: "1rem" }}>
            <strong>Recommended Roles:</strong>
            <ul style={{ marginTop: "0.5rem", paddingLeft: "1.5rem" }}>
              {message.data.recommended_roles.map((role: any, idx: number) => (
                <li key={idx}>{role.title}</li>
              ))}
            </ul>
          </div>
        )}

        {message.data?.jobs && message.data.jobs.length > 0 && (
          <div style={{ marginTop: "1.5rem" }}>
            <strong style={{ fontSize: "1rem", color: "inherit" }}>
              💼 Job Opportunities:
            </strong>
            <div
              style={{
                marginTop: "1rem",
                display: "flex",
                flexDirection: "column",
                gap: "0.75rem",
              }}
            >
              {message.data.jobs.slice(0, 3).map((job: any, idx: number) => (
                <div
                  key={idx}
                  className="hover-lift"
                  style={{
                    padding: "1rem",
                    background:
                      "linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(5, 150, 105, 0.05) 100%)",
                    borderRadius: "var(--radius-md)",
                    border: "2px solid rgba(16, 185, 129, 0.2)",
                    transition: "all 0.3s ease",
                  }}
                >
                  <div style={{ marginBottom: "0.75rem" }}>
                    <div
                      style={{
                        fontWeight: 700,
                        fontSize: "1rem",
                        marginBottom: "0.25rem",
                      }}
                    >
                      {job.title}
                    </div>
                    <div
                      style={{
                        color: "var(--primary)",
                        fontWeight: 600,
                        fontSize: "0.9rem",
                      }}
                    >
                      {job.company}
                    </div>
                    {job.location && (
                      <div
                        style={{
                          color: "var(--gray-600)",
                          fontSize: "0.85rem",
                          marginTop: "0.25rem",
                        }}
                      >
                        📍 {job.location}
                      </div>
                    )}
                    <div
                      style={{
                        display: "inline-block",
                        marginTop: "0.5rem",
                        padding: "0.25rem 0.75rem",
                        background:
                          (job.match_score || 0.01) >= 0.5
                            ? "rgba(16, 185, 129, 0.1)"
                            : (job.match_score || 0.01) >= 0.3
                            ? "rgba(245, 158, 11, 0.1)"
                            : "rgba(239, 68, 68, 0.1)",
                        borderRadius: "var(--radius-full)",
                        fontSize: "0.75rem",
                        fontWeight: 600,
                        color:
                          (job.match_score || 0.01) >= 0.5
                            ? "var(--success)"
                            : (job.match_score || 0.01) >= 0.3
                            ? "var(--warning)"
                            : "var(--danger)",
                      }}
                    >
                      {Math.round((job.match_score || 0.01) * 100)}% match
                    </div>
                  </div>
                  {job.url && (
                    <a
                      href={job.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "0.5rem",
                        padding: "0.5rem 1rem",
                        background:
                          job.source === "linkedin"
                            ? "linear-gradient(135deg, #0077b5 0%, #005885 100%)"
                            : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color: "white",
                        textDecoration: "none",
                        borderRadius: "var(--radius-md)",
                        fontSize: "0.875rem",
                        fontWeight: 600,
                        transition: "all 0.3s ease",
                        boxShadow: "var(--shadow-sm)",
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = "translateY(-2px)";
                        e.currentTarget.style.boxShadow = "var(--shadow-md)";
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = "translateY(0)";
                        e.currentTarget.style.boxShadow = "var(--shadow-sm)";
                      }}
                    >
                      {job.source === "linkedin"
                        ? "🔗 View on LinkedIn"
                        : "🔍 Search Jobs"}{" "}
                      →
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {message.data?.learning_roadmap && (
          <div style={{ marginTop: "1.5rem" }}>
            <div
              style={{
                padding: "1.5rem",
                background:
                  "linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)",
                borderRadius: "var(--radius-lg)",
                border: "2px solid rgba(102, 126, 234, 0.2)",
              }}
            >
              <div style={{ marginBottom: "1rem" }}>
                <strong style={{ fontSize: "1.1rem", color: "var(--primary)" }}>
                  📚 Learning Roadmap
                </strong>
                {message.data.learning_roadmap.target_role && (
                  <div
                    style={{
                      marginTop: "0.5rem",
                      color: "var(--gray-600)",
                      fontSize: "0.9rem",
                    }}
                  >
                    Target Role:{" "}
                    <strong>{message.data.learning_roadmap.target_role}</strong>
                  </div>
                )}
                {message.data.learning_roadmap.skill && (
                  <div
                    style={{
                      marginTop: "0.5rem",
                      color: "var(--gray-600)",
                      fontSize: "0.9rem",
                    }}
                  >
                    Skill:{" "}
                    <strong>{message.data.learning_roadmap.skill}</strong>
                  </div>
                )}
                <div
                  style={{
                    marginTop: "0.5rem",
                    color: "var(--gray-600)",
                    fontSize: "0.9rem",
                  }}
                >
                  Total:{" "}
                  <strong>
                    {message.data.learning_roadmap.total_weeks} weeks
                  </strong>{" "}
                  ({message.data.learning_roadmap.estimated_total_hours} hours)
                </div>
              </div>

              {message.data.learning_roadmap.weeks &&
                message.data.learning_roadmap.weeks.length > 0 && (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "1rem",
                    }}
                  >
                    {message.data.learning_roadmap.weeks.map(
                      (week: any, idx: number) => (
                        <div
                          key={idx}
                          style={{
                            padding: "1rem",
                            background: "white",
                            borderRadius: "var(--radius-md)",
                            border: "1px solid rgba(102, 126, 234, 0.1)",
                            boxShadow: "var(--shadow-sm)",
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
                                  fontSize: "1rem",
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
                              {week.hours} hours
                            </div>
                          </div>
                          <div style={{ marginTop: "0.75rem" }}>
                            <div
                              style={{
                                fontSize: "0.9rem",
                                fontWeight: 600,
                                marginBottom: "0.5rem",
                                color: "var(--gray-700)",
                              }}
                            >
                              Topics to Study:
                            </div>
                            <ul
                              style={{
                                margin: 0,
                                paddingLeft: "1.5rem",
                                color: "var(--gray-700)",
                              }}
                            >
                              {week.topics.map(
                                (topic: string, topicIdx: number) => (
                                  <li
                                    key={topicIdx}
                                    style={{
                                      marginBottom: "0.25rem",
                                      fontSize: "0.875rem",
                                    }}
                                  >
                                    {topic}
                                  </li>
                                )
                              )}
                            </ul>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                )}

              {message.data.learning_roadmap.prerequisites &&
                message.data.learning_roadmap.prerequisites.missing &&
                message.data.learning_roadmap.prerequisites.missing.length >
                  0 && (
                  <div
                    style={{
                      marginTop: "1rem",
                      padding: "0.75rem",
                      background: "rgba(245, 158, 11, 0.1)",
                      borderRadius: "var(--radius-md)",
                      border: "1px solid rgba(245, 158, 11, 0.2)",
                    }}
                  >
                    <div
                      style={{
                        fontSize: "0.9rem",
                        fontWeight: 600,
                        marginBottom: "0.5rem",
                        color: "var(--warning)",
                      }}
                    >
                      ⚠️ Prerequisites to Learn First:
                    </div>
                    <div
                      style={{ fontSize: "0.85rem", color: "var(--gray-700)" }}
                    >
                      {message.data.learning_roadmap.prerequisites.missing.join(
                        ", "
                      )}
                    </div>
                  </div>
                )}
            </div>
          </div>
        )}

        {message.data?.learning_resources &&
          message.data.learning_resources.length > 0 && (
            <div style={{ marginTop: "1.5rem" }}>
              <strong style={{ fontSize: "1rem", color: "inherit" }}>
                📚 Learning Resources:
              </strong>
              <div
                style={{
                  marginTop: "1rem",
                  display: "flex",
                  flexDirection: "column",
                  gap: "0.75rem",
                }}
              >
                {message.data.learning_resources
                  .slice(0, 5)
                  .map((resource: any, idx: number) => (
                    <div
                      key={idx}
                      className="hover-lift"
                      style={{
                        padding: "1rem",
                        background:
                          resource.provider === "YouTube"
                            ? "linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(220, 38, 38, 0.05) 100%)"
                            : "linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(79, 70, 229, 0.05) 100%)",
                        borderRadius: "var(--radius-md)",
                        border: `2px solid ${
                          resource.provider === "YouTube"
                            ? "rgba(239, 68, 68, 0.2)"
                            : "rgba(99, 102, 241, 0.2)"
                        }`,
                        transition: "all 0.3s ease",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "start",
                          gap: "1rem",
                        }}
                      >
                        <div style={{ flex: 1 }}>
                          <div
                            style={{
                              fontWeight: 600,
                              marginBottom: "0.25rem",
                              fontSize: "0.95rem",
                            }}
                          >
                            {resource.title}
                          </div>
                          {resource.description && (
                            <div
                              style={{
                                color: "var(--gray-600)",
                                fontSize: "0.85rem",
                                marginTop: "0.25rem",
                              }}
                            >
                              {resource.description.substring(0, 100)}...
                            </div>
                          )}
                          {resource.missing_skill && (
                            <div
                              style={{
                                display: "inline-block",
                                marginTop: "0.5rem",
                                padding: "0.25rem 0.75rem",
                                background: "rgba(245, 158, 11, 0.1)",
                                borderRadius: "var(--radius-full)",
                                fontSize: "0.75rem",
                                fontWeight: 600,
                                color: "var(--warning)",
                              }}
                            >
                              Addresses: {resource.missing_skill}
                            </div>
                          )}
                        </div>
                        {resource.provider && (
                          <span
                            style={{
                              padding: "0.375rem 0.75rem",
                              background:
                                resource.provider === "YouTube"
                                  ? "#FF0000"
                                  : "var(--gray-500)",
                              color: "white",
                              borderRadius: "var(--radius-full)",
                              fontSize: "0.75rem",
                              fontWeight: 600,
                              textTransform: "uppercase",
                              letterSpacing: "0.5px",
                            }}
                          >
                            📺 {resource.provider}
                          </span>
                        )}
                      </div>
                      <a
                        href={resource.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          display: "inline-flex",
                          alignItems: "center",
                          gap: "0.5rem",
                          marginTop: "0.75rem",
                          padding: "0.5rem 1rem",
                          background:
                            resource.provider === "YouTube"
                              ? "linear-gradient(135deg, #FF0000 0%, #CC0000 100%)"
                              : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                          color: "white",
                          textDecoration: "none",
                          borderRadius: "var(--radius-md)",
                          fontSize: "0.875rem",
                          fontWeight: 600,
                          transition: "all 0.3s ease",
                          boxShadow: "var(--shadow-sm)",
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = "translateY(-2px)";
                          e.currentTarget.style.boxShadow = "var(--shadow-md)";
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = "translateY(0)";
                          e.currentTarget.style.boxShadow = "var(--shadow-sm)";
                        }}
                      >
                        {resource.provider === "YouTube"
                          ? "📺 Watch on YouTube"
                          : "Start Learning"}{" "}
                        →
                      </a>
                    </div>
                  ))}
              </div>
            </div>
          )}

        {message.data?.skill_gap && (
          <div style={{ marginTop: "1rem" }}>
            <strong>Skill Gap Analysis:</strong>
            <div style={{ marginTop: "0.5rem" }}>
              <p>
                Match: {Math.round(message.data.skill_gap.match_percentage)}%
              </p>
              <p>
                Matching Skills:{" "}
                {message.data.skill_gap.matching_skills?.length || 0}
              </p>
              <p>
                Missing Skills:{" "}
                {message.data.skill_gap.missing_skills?.length || 0}
              </p>
            </div>
          </div>
        )}
      </div>
    );
  };

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
            💬 Career Guidance Chatbot
          </h1>
          <p style={{ fontSize: "1.1rem", opacity: 0.95 }}>
            Ask me anything about your career, skills, jobs, or learning paths
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

      <div
        className="card"
        style={{
          maxWidth: "900px",
          margin: "0 auto",
          height: "650px",
          display: "flex",
          flexDirection: "column",
          padding: 0,
          overflow: "hidden",
        }}
      >
        {/* Messages area */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            marginBottom: "1rem",
            padding: "1.5rem",
            background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
            borderRadius: "var(--radius-lg)",
            position: "relative",
          }}
        >
          {messages.map((message) => (
            <div
              key={message.id}
              style={{
                marginBottom: "1rem",
                display: "flex",
                justifyContent:
                  message.sender === "user" ? "flex-end" : "flex-start",
              }}
            >
              <div
                style={{
                  maxWidth: "75%",
                  padding: "1rem 1.25rem",
                  borderRadius:
                    message.sender === "user"
                      ? "var(--radius-lg) var(--radius-lg) var(--radius-lg) 0"
                      : "var(--radius-lg) var(--radius-lg) 0 var(--radius-lg)",
                  background:
                    message.sender === "user"
                      ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                      : "white",
                  color:
                    message.sender === "user" ? "white" : "var(--gray-900)",
                  whiteSpace: "pre-wrap",
                  wordWrap: "break-word",
                  boxShadow:
                    message.sender === "user"
                      ? "0 4px 15px rgba(102, 126, 234, 0.3)"
                      : "var(--shadow-md)",
                  animation: "slideUp 0.3s ease",
                  position: "relative",
                }}
              >
                {renderMessageContent(message)}

                {/* Suggestions */}
                {message.suggestions && message.suggestions.length > 0 && (
                  <div
                    style={{
                      marginTop: "1rem",
                      display: "flex",
                      flexWrap: "wrap",
                      gap: "0.5rem",
                    }}
                  >
                    {message.suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSuggestionClick(suggestion)}
                        style={{
                          padding: "0.5rem 1rem",
                          fontSize: "0.875rem",
                          background:
                            message.sender === "user"
                              ? "rgba(255,255,255,0.2)"
                              : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                          color: "white",
                          border: "none",
                          borderRadius: "var(--radius-full)",
                          cursor: "pointer",
                          transition: "all 0.3s ease",
                          fontWeight: 500,
                          boxShadow: "var(--shadow-sm)",
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = "translateY(-2px)";
                          e.currentTarget.style.boxShadow = "var(--shadow-md)";
                          e.currentTarget.style.background =
                            message.sender === "user"
                              ? "rgba(255,255,255,0.3)"
                              : "linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)";
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = "translateY(0)";
                          e.currentTarget.style.boxShadow = "var(--shadow-sm)";
                          e.currentTarget.style.background =
                            message.sender === "user"
                              ? "rgba(255,255,255,0.2)"
                              : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
                        }}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div
              style={{
                display: "flex",
                justifyContent: "flex-start",
                alignItems: "center",
                gap: "0.75rem",
              }}
            >
              <div
                style={{
                  padding: "1rem 1.25rem",
                  borderRadius: "var(--radius-lg)",
                  background: "white",
                  color: "var(--gray-700)",
                  boxShadow: "var(--shadow-md)",
                  display: "flex",
                  alignItems: "center",
                  gap: "0.75rem",
                }}
              >
                <span
                  className="spinner"
                  style={{ width: "20px", height: "20px", borderWidth: "2px" }}
                ></span>
                <span style={{ fontWeight: 500 }}>Thinking...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div
          style={{
            display: "flex",
            gap: "0.75rem",
            padding: "1rem",
            background: "white",
            borderRadius: "var(--radius-lg)",
            boxShadow: "var(--shadow-md)",
          }}
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about careers, jobs, skills, or learning paths..."
            style={{
              flex: 1,
              padding: "1rem 1.25rem",
              border: "2px solid var(--gray-200)",
              borderRadius: "var(--radius-md)",
              fontSize: "1rem",
              transition: "all 0.3s ease",
              background: "var(--gray-50)",
            }}
            onFocus={(e) => {
              e.currentTarget.style.borderColor = "var(--primary)";
              e.currentTarget.style.background = "white";
              e.currentTarget.style.boxShadow =
                "0 0 0 3px rgba(99, 102, 241, 0.1)";
            }}
            onBlur={(e) => {
              e.currentTarget.style.borderColor = "var(--gray-200)";
              e.currentTarget.style.background = "var(--gray-50)";
              e.currentTarget.style.boxShadow = "none";
            }}
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="btn btn-primary"
            style={{
              padding: "1rem 2rem",
              fontSize: "1rem",
              fontWeight: 600,
              minWidth: "120px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "0.5rem",
            }}
          >
            {loading ? (
              <>
                <span
                  className="spinner"
                  style={{ width: "16px", height: "16px", borderWidth: "2px" }}
                ></span>
                Sending...
              </>
            ) : (
              <>Send →</>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
