from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile information
    full_name = db.Column(db.String(200))
    location = db.Column(db.String(200))  # User location (city, state, country)
    skills = db.Column(db.JSON)  # List of skills with proficiency levels
    experience_years = db.Column(db.Integer, default=0)
    education = db.Column(db.JSON)  # List of education entries
    interests = db.Column(db.JSON)  # List of interests/goals
    current_role = db.Column(db.String(200))
    target_role = db.Column(db.String(200))
    
    # Relationships
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'location': self.location,
            'skills': self.skills or [],
            'experience_years': self.experience_years,
            'education': self.education or [],
            'interests': self.interests or [],
            'current_role': self.current_role,
            'target_role': self.target_role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Job(db.Model):
    """Job posting model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    description = db.Column(db.Text)
    required_skills = db.Column(db.JSON)  # List of required skills
    location = db.Column(db.String(200))
    salary_range = db.Column(db.String(100))
    job_type = db.Column(db.String(50))  # full-time, part-time, contract
    experience_level = db.Column(db.String(50))  # entry, mid, senior
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'required_skills': self.required_skills or [],
            'location': self.location,
            'salary_range': self.salary_range,
            'job_type': self.job_type,
            'experience_level': self.experience_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CareerRole(db.Model):
    """Career role model"""
    __tablename__ = 'career_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.JSON)  # List of required skills with importance
    category = db.Column(db.String(100))  # e.g., "Software Engineering", "Data Science"
    average_salary = db.Column(db.String(100))
    growth_outlook = db.Column(db.String(50))  # high, medium, low
    typical_path = db.Column(db.JSON)  # Career progression path
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'required_skills': self.required_skills or [],
            'category': self.category,
            'average_salary': self.average_salary,
            'growth_outlook': self.growth_outlook,
            'typical_path': self.typical_path or []
        }

class LearningResource(db.Model):
    """Learning resource model"""
    __tablename__ = 'learning_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50))  # course, article, video, book
    url = db.Column(db.String(500))
    skills_covered = db.Column(db.JSON)  # List of skills this resource teaches
    difficulty_level = db.Column(db.String(50))  # beginner, intermediate, advanced
    duration = db.Column(db.String(100))  # e.g., "10 hours", "4 weeks"
    provider = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'resource_type': self.resource_type,
            'url': self.url,
            'skills_covered': self.skills_covered or [],
            'difficulty_level': self.difficulty_level,
            'duration': self.duration,
            'provider': self.provider
        }

class Feedback(db.Model):
    """User feedback on recommendations"""
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_type = db.Column(db.String(50))  # job, role, resource
    item_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 or -1/1 for thumbs up/down
    feedback_type = db.Column(db.String(50))  # click, save, like, dislike
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'rating': self.rating,
            'feedback_type': self.feedback_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class QuizResult(db.Model):
    """Quiz results for skill verification"""
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)  # 0-100
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill': self.skill,
            'score': self.score,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

