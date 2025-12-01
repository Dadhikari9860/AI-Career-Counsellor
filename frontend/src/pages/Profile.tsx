import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import "../App.css";

const Profile: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [formData, setFormData] = useState({
    full_name: user?.full_name || "",
    location: user?.location || "",
    skills: user?.skills || [],
    experience_years: user?.experience_years || 0,
    current_role: user?.current_role || "",
    target_role: user?.target_role || "",
    interests: user?.interests || [],
  });
  const [newSkill, setNewSkill] = useState("");
  const [newInterest, setNewInterest] = useState("");
  const [message, setMessage] = useState("");
  const [availableRoles, setAvailableRoles] = useState<string[]>([]);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeUploading, setResumeUploading] = useState(false);
  const [resumeData, setResumeData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<"profile" | "resume">("profile");

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || "",
        location: user.location || "",
        skills: user.skills || [],
        experience_years: user.experience_years || 0,
        current_role: user.current_role || "",
        target_role: user.target_role || "",
        interests: user.interests || [],
      });
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.put("/profile", formData);
      updateUser(response.data.user);
      setMessage("Profile updated successfully!");
      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      setMessage("Failed to update profile");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      setMessage("Please select a file");
      return;
    }

    setResumeUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("resume", resumeFile);

    try {
      const response = await api.post("/resume/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 30000, // 30 second timeout for file upload
      });

      setResumeData(response.data);
      setMessage("Resume uploaded and parsed successfully!");

      // Update user profile with parsed data
      if (response.data.user_updated) {
        updateUser(response.data.user_updated);
        // Update form data
        setFormData((prev) => ({
          ...prev,
          skills: response.data.user_updated.skills || prev.skills,
          experience_years:
            response.data.user_updated.experience_years ||
            prev.experience_years,
          current_role:
            response.data.user_updated.current_role || prev.current_role,
          location: response.data.user_updated.location || prev.location,
        }));
      }

      setTimeout(() => setMessage(""), 5000);
    } catch (error: any) {
      setMessage(error.response?.data?.error || "Failed to upload resume");
      setTimeout(() => setMessage(""), 3000);
    } finally {
      setResumeUploading(false);
    }
  };

  const addSkill = () => {
    if (newSkill.trim()) {
      setFormData({
        ...formData,
        skills: [...formData.skills, newSkill.trim()],
      });
      setNewSkill("");
    }
  };

  const removeSkill = (index: number) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter((_, i) => i !== index),
    });
  };

  const addInterest = () => {
    if (newInterest.trim()) {
      setFormData({
        ...formData,
        interests: [...formData.interests, newInterest.trim()],
      });
      setNewInterest("");
    }
  };

  const removeInterest = (index: number) => {
    setFormData({
      ...formData,
      interests: formData.interests.filter((_, i) => i !== index),
    });
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
            👤 My Profile
          </h1>
          <p style={{ fontSize: "1.1rem", opacity: 0.95 }}>
            Manage your profile information and upload your resume
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

      {/* Tabs */}
      <div
        style={{
          display: "flex",
          gap: "0.5rem",
          marginBottom: "2rem",
          background: "white",
          padding: "0.5rem",
          borderRadius: "var(--radius-lg)",
          boxShadow: "var(--shadow-md)",
        }}
      >
        <button
          onClick={() => setActiveTab("profile")}
          style={{
            padding: "0.875rem 1.75rem",
            background:
              activeTab === "profile"
                ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                : "transparent",
            color: activeTab === "profile" ? "white" : "var(--gray-700)",
            border: "none",
            borderRadius: "var(--radius-md)",
            cursor: "pointer",
            fontSize: "1rem",
            fontWeight: activeTab === "profile" ? 600 : 500,
            transition: "all 0.3s ease",
            boxShadow: activeTab === "profile" ? "var(--shadow)" : "none",
          }}
        >
          📝 Profile Information
        </button>
        <button
          onClick={() => setActiveTab("resume")}
          style={{
            padding: "0.875rem 1.75rem",
            background:
              activeTab === "resume"
                ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                : "transparent",
            color: activeTab === "resume" ? "white" : "var(--gray-700)",
            border: "none",
            borderRadius: "var(--radius-md)",
            cursor: "pointer",
            fontSize: "1rem",
            fontWeight: activeTab === "resume" ? 600 : 500,
            transition: "all 0.3s ease",
            boxShadow: activeTab === "resume" ? "var(--shadow)" : "none",
          }}
        >
          📄 Resume Upload
        </button>
      </div>

      {message && (
        <div
          style={{
            padding: "1rem",
            marginBottom: "1rem",
            background: message.includes("success") ? "#d4edda" : "#f8d7da",
            color: message.includes("success") ? "#155724" : "#721c24",
            borderRadius: "4px",
          }}
        >
          {message}
        </div>
      )}

      {activeTab === "profile" ? (
        <form
          onSubmit={handleSubmit}
          style={{ maxWidth: "800px", margin: "0 auto" }}
        >
          <div className="card">
            <h2>Personal Information</h2>

            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) =>
                  setFormData({ ...formData, full_name: e.target.value })
                }
                placeholder="Enter your full name"
              />
            </div>

            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) =>
                  setFormData({ ...formData, location: e.target.value })
                }
                placeholder="e.g., New York, NY or San Francisco, CA"
              />
              <small
                style={{
                  color: "#666",
                  marginTop: "0.25rem",
                  display: "block",
                }}
              >
                Enter your city and state/country to find jobs nearby
              </small>
            </div>

            <div className="form-group">
              <label>Current Role</label>
              <input
                type="text"
                value={formData.current_role}
                onChange={(e) =>
                  setFormData({ ...formData, current_role: e.target.value })
                }
                placeholder="e.g., Software Engineer"
              />
            </div>

            <div className="form-group">
              <label>Experience (Years)</label>
              <input
                type="number"
                min="0"
                max="50"
                value={formData.experience_years}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    experience_years: parseInt(e.target.value) || 0,
                  })
                }
              />
            </div>

            <div className="form-group">
              <label>Target Role</label>
              {availableRoles.length > 0 ? (
                <select
                  value={formData.target_role}
                  onChange={(e) =>
                    setFormData({ ...formData, target_role: e.target.value })
                  }
                  style={{ padding: "0.75rem", width: "100%" }}
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
                  value={formData.target_role}
                  onChange={(e) =>
                    setFormData({ ...formData, target_role: e.target.value })
                  }
                  placeholder="e.g., Full Stack Developer"
                  list="role-suggestions"
                />
              )}
              <datalist id="role-suggestions">
                {availableRoles.map((role) => (
                  <option key={role} value={role} />
                ))}
              </datalist>
              {availableRoles.length > 0 && (
                <small
                  style={{
                    color: "#666",
                    marginTop: "0.25rem",
                    display: "block",
                  }}
                >
                  Available roles: {availableRoles.join(", ")}
                </small>
              )}
            </div>
          </div>

          <div className="card" style={{ marginTop: "1.5rem" }}>
            <h2>Skills</h2>
            <div className="form-group">
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <input
                  type="text"
                  value={newSkill}
                  onChange={(e) => setNewSkill(e.target.value)}
                  onKeyPress={(e) =>
                    e.key === "Enter" && (e.preventDefault(), addSkill())
                  }
                  placeholder="Add a skill (e.g., Python, React)"
                  style={{ flex: 1 }}
                />
                <button
                  type="button"
                  onClick={addSkill}
                  className="btn btn-secondary"
                >
                  Add
                </button>
              </div>
            </div>
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "0.5rem",
                marginTop: "1rem",
              }}
            >
              {formData.skills.map((skill, index) => (
                <span
                  key={index}
                  style={{
                    padding: "0.5rem 1rem",
                    background: "#007bff",
                    color: "white",
                    borderRadius: "20px",
                    display: "flex",
                    alignItems: "center",
                    gap: "0.5rem",
                  }}
                >
                  {typeof skill === "string" ? skill : skill.name || skill}
                  <button
                    type="button"
                    onClick={() => removeSkill(index)}
                    style={{
                      background: "rgba(255,255,255,0.3)",
                      border: "none",
                      color: "white",
                      cursor: "pointer",
                      borderRadius: "50%",
                      width: "20px",
                      height: "20px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          <div className="card" style={{ marginTop: "1.5rem" }}>
            <h2>Interests</h2>
            <div className="form-group">
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <input
                  type="text"
                  value={newInterest}
                  onChange={(e) => setNewInterest(e.target.value)}
                  onKeyPress={(e) =>
                    e.key === "Enter" && (e.preventDefault(), addInterest())
                  }
                  placeholder="Add an interest"
                  style={{ flex: 1 }}
                />
                <button
                  type="button"
                  onClick={addInterest}
                  className="btn btn-secondary"
                >
                  Add
                </button>
              </div>
            </div>
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "0.5rem",
                marginTop: "1rem",
              }}
            >
              {formData.interests.map((interest, index) => (
                <span
                  key={index}
                  style={{
                    padding: "0.5rem 1rem",
                    background: "#28a745",
                    color: "white",
                    borderRadius: "20px",
                    display: "flex",
                    alignItems: "center",
                    gap: "0.5rem",
                  }}
                >
                  {interest}
                  <button
                    type="button"
                    onClick={() => removeInterest(index)}
                    style={{
                      background: "rgba(255,255,255,0.3)",
                      border: "none",
                      color: "white",
                      cursor: "pointer",
                      borderRadius: "50%",
                      width: "20px",
                      height: "20px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ marginTop: "1.5rem" }}
          >
            Save Profile
          </button>
        </form>
      ) : (
        <div style={{ maxWidth: "800px", margin: "0 auto" }}>
          <div className="card">
            <h2>Upload Resume</h2>
            <p style={{ color: "#666", marginBottom: "1.5rem" }}>
              Upload your resume (PDF, DOC, DOCX, or TXT) to automatically
              extract your skills, experience, and other information. This will
              help us provide better job recommendations.
            </p>

            <div className="form-group">
              <label>Select Resume File</label>
              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
                style={{ padding: "0.5rem" }}
              />
              {resumeFile && (
                <p style={{ marginTop: "0.5rem", color: "#28a745" }}>
                  Selected: {resumeFile.name}
                </p>
              )}
            </div>

            <button
              onClick={handleResumeUpload}
              disabled={!resumeFile || resumeUploading}
              className="btn btn-primary"
              style={{
                opacity: !resumeFile || resumeUploading ? 0.6 : 1,
                cursor:
                  !resumeFile || resumeUploading ? "not-allowed" : "pointer",
              }}
            >
              {resumeUploading ? "Uploading..." : "Upload & Parse Resume"}
            </button>

            {resumeData && (
              <div style={{ marginTop: "2rem" }}>
                <h3>Parsed Resume Data</h3>
                <div className="card" style={{ background: "#f8f9fa" }}>
                  <div style={{ marginBottom: "1rem" }}>
                    <strong>Skills Found:</strong>
                    <div
                      style={{
                        marginTop: "0.5rem",
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "0.5rem",
                      }}
                    >
                      {resumeData.parsed_data?.skills?.map(
                        (skill: string, idx: number) => (
                          <span
                            key={idx}
                            style={{
                              padding: "0.25rem 0.75rem",
                              background: "#007bff",
                              color: "white",
                              borderRadius: "12px",
                              fontSize: "0.9rem",
                            }}
                          >
                            {skill}
                          </span>
                        )
                      )}
                    </div>
                  </div>

                  {resumeData.parsed_data?.experience_years && (
                    <div style={{ marginBottom: "1rem" }}>
                      <strong>Experience:</strong>{" "}
                      {resumeData.parsed_data.experience_years} years
                    </div>
                  )}

                  {resumeData.parsed_data?.current_role && (
                    <div style={{ marginBottom: "1rem" }}>
                      <strong>Current Role:</strong>{" "}
                      {resumeData.parsed_data.current_role}
                    </div>
                  )}

                  {resumeData.parsed_data?.education &&
                    resumeData.parsed_data.education.length > 0 && (
                      <div style={{ marginBottom: "1rem" }}>
                        <strong>Education:</strong>{" "}
                        {resumeData.parsed_data.education.join(", ")}
                      </div>
                    )}

                  {resumeData.parsed_data?.location && (
                    <div style={{ marginBottom: "1rem" }}>
                      <strong>Location:</strong>{" "}
                      {resumeData.parsed_data.location}
                    </div>
                  )}

                  {resumeData.linkedin_profile_url && (
                    <div style={{ marginBottom: "1rem" }}>
                      <strong>LinkedIn Profile:</strong>{" "}
                      <a
                        href={resumeData.linkedin_profile_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          color: "#0077b5",
                          textDecoration: "none",
                          fontWeight: 600,
                        }}
                      >
                        View Profile Search →
                      </a>
                    </div>
                  )}

                  {resumeData.recommended_jobs &&
                    resumeData.recommended_jobs.length > 0 && (
                      <div style={{ marginTop: "1.5rem" }}>
                        <strong>
                          Recommended Jobs (filtered by your location):
                        </strong>
                        <div style={{ marginTop: "0.5rem" }}>
                          {resumeData.recommended_jobs.map(
                            (job: any, idx: number) => (
                              <div
                                key={idx}
                                style={{
                                  padding: "0.75rem",
                                  marginBottom: "0.5rem",
                                  background: "white",
                                  borderRadius: "4px",
                                  border: "1px solid #ddd",
                                  cursor: job.url ? "pointer" : "default",
                                  transition: "all 0.2s ease",
                                }}
                                onClick={() => {
                                  if (job.url) {
                                    window.open(
                                      job.url,
                                      "_blank",
                                      "noopener,noreferrer"
                                    );
                                  }
                                }}
                                onMouseEnter={(e) => {
                                  if (job.url) {
                                    e.currentTarget.style.background =
                                      "#f0f0f0";
                                    e.currentTarget.style.borderColor =
                                      "#0077b5";
                                  }
                                }}
                                onMouseLeave={(e) => {
                                  if (job.url) {
                                    e.currentTarget.style.background = "white";
                                    e.currentTarget.style.borderColor = "#ddd";
                                  }
                                }}
                              >
                                <div
                                  style={{
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "space-between",
                                  }}
                                >
                                  <div style={{ flex: 1 }}>
                                    <div style={{ flex: 1 }}>
                                      <div>
                                        <strong>{job.title}</strong> at{" "}
                                        {job.company}
                                        {job.location && (
                                          <span> - {job.location}</span>
                                        )}
                                        <span
                                          style={{
                                            color:
                                              (job.match_score || 0.01) >= 0.5
                                                ? "#28a745"
                                                : (job.match_score || 0.01) >=
                                                  0.3
                                                ? "#ffc107"
                                                : "#ff9800",
                                            marginLeft: "0.5rem",
                                            fontWeight: "bold",
                                          }}
                                        >
                                          (
                                          {Math.round(
                                            (job.match_score || 0.01) * 100
                                          )}
                                          % match)
                                        </span>
                                      </div>
                                      {job.matched_skills &&
                                        job.matched_skills.length > 0 && (
                                          <div
                                            style={{
                                              marginTop: "0.5rem",
                                              fontSize: "0.85rem",
                                              color: "#666",
                                            }}
                                          >
                                            <strong>Matched Skills:</strong>{" "}
                                            {job.matched_skills
                                              .slice(0, 5)
                                              .join(", ")}
                                            {job.matched_skills.length > 5 &&
                                              "..."}
                                          </div>
                                        )}
                                    </div>
                                    {job.matched_skills &&
                                      job.matched_skills.length > 0 && (
                                        <div
                                          style={{
                                            marginTop: "0.5rem",
                                            fontSize: "0.85rem",
                                            color: "#666",
                                          }}
                                        >
                                          <strong>Matched Skills:</strong>{" "}
                                          {job.matched_skills
                                            .slice(0, 5)
                                            .join(", ")}
                                          {job.matched_skills.length > 5 &&
                                            "..."}
                                        </div>
                                      )}
                                  </div>
                                  {job.url && (
                                    <span
                                      style={{
                                        color: "#0077b5",
                                        fontSize: "0.9rem",
                                        fontWeight: 600,
                                      }}
                                    >
                                      View on LinkedIn →
                                    </span>
                                  )}
                                </div>
                              </div>
                            )
                          )}
                        </div>
                      </div>
                    )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;
