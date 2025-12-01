import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import api from "../services/api";
import "../App.css";

interface Question {
  question: string;
  options: string[];
  correct: number;
}

const skillQuizzes: Record<string, Question[]> = {
  python: [
    {
      question: "What is the output of: print(2 ** 3)",
      options: ["6", "8", "9", "5"],
      correct: 1,
    },
    {
      question: "Which method is used to add an item to a list?",
      options: ["add()", "append()", "insert()", "push()"],
      correct: 1,
    },
    {
      question: "What does len() function return?",
      options: [
        "The length of a string",
        "The length of a list",
        "The number of items",
        "All of the above",
      ],
      correct: 3,
    },
    {
      question: "What is a dictionary in Python?",
      options: [
        "A list of keys",
        "A key-value pair collection",
        "A set of values",
        "A tuple",
      ],
      correct: 1,
    },
    {
      question: "Which keyword is used for defining a function?",
      options: ["func", "def", "function", "define"],
      correct: 1,
    },
  ],
  javascript: [
    {
      question: "What is the output of: typeof null",
      options: ["null", "object", "undefined", "boolean"],
      correct: 1,
    },
    {
      question:
        "Which method creates a new array with results of calling a function?",
      options: ["forEach()", "map()", "filter()", "reduce()"],
      correct: 1,
    },
    {
      question: "What is a closure in JavaScript?",
      options: [
        "A function inside another function",
        "A variable scope",
        "A function with access to outer scope",
        "A callback",
      ],
      correct: 2,
    },
    {
      question: "What does === operator check?",
      options: ["Value only", "Type only", "Value and type", "Reference"],
      correct: 2,
    },
    {
      question: "What is the purpose of async/await?",
      options: [
        "Synchronous code",
        "Asynchronous code",
        "Error handling",
        "Looping",
      ],
      correct: 1,
    },
  ],
  "machine learning": [
    {
      question: "What is overfitting?",
      options: [
        "Model too simple",
        "Model too complex",
        "Model perfect",
        "Model broken",
      ],
      correct: 1,
    },
    {
      question: "What is cross-validation used for?",
      options: ["Training", "Testing", "Model evaluation", "Data cleaning"],
      correct: 2,
    },
    {
      question: "What is the purpose of a train/test split?",
      options: [
        "Speed up training",
        "Evaluate model performance",
        "Reduce data",
        "Increase accuracy",
      ],
      correct: 1,
    },
    {
      question: "What is a feature in machine learning?",
      options: ["A label", "An input variable", "An output", "A model"],
      correct: 1,
    },
    {
      question: "What does accuracy measure?",
      options: ["Speed", "Correct predictions", "Complexity", "Size"],
      correct: 1,
    },
  ],
};

const Quiz: React.FC = () => {
  const { user } = useAuth();
  const [selectedSkill, setSelectedSkill] = useState("python");
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [score, setScore] = useState(0);
  const [quizStarted, setQuizStarted] = useState(false);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const availableSkills = Object.keys(skillQuizzes);
  const questions = skillQuizzes[selectedSkill] || [];

  const startQuiz = () => {
    setQuizStarted(true);
    setCurrentQuestion(0);
    setScore(0);
    setSelectedAnswer(null);
    setQuizCompleted(false);
  };

  const handleAnswer = (answerIndex: number) => {
    setSelectedAnswer(answerIndex);
  };

  const handleNext = () => {
    if (selectedAnswer === null) return;

    if (selectedAnswer === questions[currentQuestion].correct) {
      setScore(score + 1);
    }

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
    } else {
      setQuizCompleted(true);
      submitQuiz();
    }
  };

  const submitQuiz = async () => {
    setSubmitting(true);
    const finalScore = (score / questions.length) * 100;

    try {
      await api.post("/quiz/submit", {
        skill: selectedSkill,
        score: finalScore,
        total_questions: questions.length,
        correct_answers: score,
      });
    } catch (error) {
      console.error("Failed to submit quiz:", error);
    } finally {
      setSubmitting(false);
    }
  };

  const resetQuiz = () => {
    setQuizStarted(false);
    setQuizCompleted(false);
    setCurrentQuestion(0);
    setScore(0);
    setSelectedAnswer(null);
  };

  if (!quizStarted) {
    return (
      <div className="container">
        <div className="card">
          <h2>Skill Verification Quiz</h2>
          <p>Test your knowledge and update your skill proficiency</p>

          <div className="form-group">
            <label>Select a Skill to Test</label>
            <select
              value={selectedSkill}
              onChange={(e) => setSelectedSkill(e.target.value)}
              style={{ padding: "0.75rem" }}
            >
              {availableSkills.map((skill) => (
                <option key={skill} value={skill}>
                  {skill.charAt(0).toUpperCase() + skill.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div style={{ marginTop: "1rem" }}>
            <p>
              <strong>Quiz Details:</strong>
            </p>
            <ul>
              <li>
                Skill:{" "}
                {selectedSkill.charAt(0).toUpperCase() + selectedSkill.slice(1)}
              </li>
              <li>Number of Questions: {questions.length}</li>
              <li>Time: ~5 minutes</li>
            </ul>
          </div>

          <button
            onClick={startQuiz}
            className="btn btn-primary"
            style={{ marginTop: "1rem" }}
          >
            Start Quiz
          </button>
        </div>
      </div>
    );
  }

  if (quizCompleted) {
    const finalScore =
      ((score +
        (selectedAnswer === questions[currentQuestion].correct ? 1 : 0)) /
        questions.length) *
      100;
    return (
      <div className="container">
        <div className="card">
          <h2>Quiz Completed!</h2>
          <div style={{ textAlign: "center", padding: "2rem" }}>
            <h3 style={{ fontSize: "3rem", color: "#28a745" }}>
              {Math.round(finalScore)}%
            </h3>
            <p>
              You scored{" "}
              {score +
                (selectedAnswer === questions[currentQuestion].correct
                  ? 1
                  : 0)}{" "}
              out of {questions.length}
            </p>
            {submitting && <p>Updating your profile...</p>}
            {!submitting && (
              <div>
                <p className="success">
                  Your skill proficiency has been updated!
                </p>
                <button
                  onClick={resetQuiz}
                  className="btn btn-primary"
                  style={{ marginTop: "1rem" }}
                >
                  Take Another Quiz
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];

  return (
    <div className="container">
      <div className="card">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "1rem",
          }}
        >
          <h2>
            {selectedSkill.charAt(0).toUpperCase() + selectedSkill.slice(1)}{" "}
            Quiz
          </h2>
          <span>
            Question {currentQuestion + 1} of {questions.length}
          </span>
        </div>

        <div style={{ marginBottom: "2rem" }}>
          <h3>{question.question}</h3>
        </div>

        <div
          style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}
        >
          {question.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswer(index)}
              style={{
                padding: "1rem",
                textAlign: "left",
                border: "2px solid",
                borderColor: selectedAnswer === index ? "#007bff" : "#ddd",
                borderRadius: "4px",
                background: selectedAnswer === index ? "#e7f3ff" : "white",
                cursor: "pointer",
                fontSize: "1rem",
              }}
            >
              {String.fromCharCode(65 + index)}. {option}
            </button>
          ))}
        </div>

        <button
          onClick={handleNext}
          className="btn btn-primary"
          disabled={selectedAnswer === null}
          style={{ marginTop: "1rem", width: "100%" }}
        >
          {currentQuestion < questions.length - 1 ? "Next" : "Finish Quiz"}
        </button>
      </div>
    </div>
  );
};

export default Quiz;
