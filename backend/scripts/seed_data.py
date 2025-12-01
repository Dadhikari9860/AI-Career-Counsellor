"""
Script to seed database with sample data for testing
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import User, Job, CareerRole, LearningResource
from config import Config

def seed_data():
    """Seed database with sample data"""
    app = create_app(Config)
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        # db.drop_all()
        # db.create_all()
        
        # Create career roles
        roles = [
            CareerRole(
                title='Data Scientist',
                description='Analyze complex data to help organizations make data-driven decisions',
                required_skills=['python', 'machine learning', 'sql', 'statistics', 'data visualization'],
                category='Data Science',
                average_salary='$120,000',
                growth_outlook='high',
                typical_path=[
                    {'level': 'Junior Data Scientist', 'years': 0, 'skills': ['python', 'sql', 'pandas']},
                    {'level': 'Data Scientist', 'years': 2, 'skills': ['machine learning', 'statistics', 'scikit-learn']},
                    {'level': 'Senior Data Scientist', 'years': 5, 'skills': ['deep learning', 'mlops', 'leadership']},
                    {'level': 'Principal Data Scientist', 'years': 8, 'skills': ['research', 'architecture', 'strategy']}
                ]
            ),
            CareerRole(
                title='Software Engineer',
                description='Design, develop, and maintain software applications',
                required_skills=['programming', 'algorithms', 'data structures', 'software design', 'testing'],
                category='Software Development',
                average_salary='$110,000',
                growth_outlook='high',
                typical_path=[
                    {'level': 'Junior Software Engineer', 'years': 0, 'skills': ['programming basics', 'git']},
                    {'level': 'Software Engineer', 'years': 2, 'skills': ['design patterns', 'testing', 'apis']},
                    {'level': 'Senior Software Engineer', 'years': 5, 'skills': ['architecture', 'mentoring', 'system design']},
                    {'level': 'Principal Engineer', 'years': 8, 'skills': ['technical leadership', 'innovation']}
                ]
            ),
            CareerRole(
                title='ML Engineer',
                description='Build and deploy machine learning models in production',
                required_skills=['python', 'machine learning', 'mlops', 'cloud', 'docker'],
                category='Machine Learning',
                average_salary='$130,000',
                growth_outlook='high',
                typical_path=[
                    {'level': 'Junior ML Engineer', 'years': 0, 'skills': ['python', 'scikit-learn']},
                    {'level': 'ML Engineer', 'years': 2, 'skills': ['tensorflow', 'pytorch', 'mlops']},
                    {'level': 'Senior ML Engineer', 'years': 5, 'skills': ['production systems', 'scaling', 'leadership']},
                    {'level': 'ML Architect', 'years': 8, 'skills': ['system design', 'research', 'strategy']}
                ]
            ),
            CareerRole(
                title='Full Stack Developer',
                description='Develop both frontend and backend of web applications',
                required_skills=['javascript', 'react', 'node.js', 'databases', 'apis'],
                category='Web Development',
                average_salary='$105,000',
                growth_outlook='high',
                typical_path=[
                    {'level': 'Junior Full Stack Developer', 'years': 0, 'skills': ['html', 'css', 'javascript']},
                    {'level': 'Full Stack Developer', 'years': 2, 'skills': ['react', 'node.js', 'databases']},
                    {'level': 'Senior Full Stack Developer', 'years': 5, 'skills': ['architecture', 'performance', 'security']},
                    {'level': 'Tech Lead', 'years': 8, 'skills': ['team leadership', 'system design']}
                ]
            ),
            CareerRole(
                title='DevOps Engineer',
                description='Manage infrastructure, CI/CD pipelines, and cloud services',
                required_skills=['docker', 'kubernetes', 'aws', 'ci/cd', 'linux'],
                category='DevOps',
                average_salary='$115,000',
                growth_outlook='high',
                typical_path=[
                    {'level': 'Junior DevOps Engineer', 'years': 0, 'skills': ['linux', 'git', 'bash']},
                    {'level': 'DevOps Engineer', 'years': 2, 'skills': ['docker', 'ci/cd', 'cloud basics']},
                    {'level': 'Senior DevOps Engineer', 'years': 5, 'skills': ['kubernetes', 'terraform', 'architecture']},
                    {'level': 'DevOps Architect', 'years': 8, 'skills': ['strategic planning', 'leadership']}
                ]
            )
        ]
        
        for role in roles:
            existing = CareerRole.query.filter_by(title=role.title).first()
            if not existing:
                db.session.add(role)
        
        # Create sample jobs
        jobs = [
            Job(
                title='Senior Data Scientist',
                company='Tech Corp',
                description='We are looking for an experienced data scientist to join our team. You will work on machine learning models, analyze large datasets, and provide insights to stakeholders.',
                required_skills=['python', 'machine learning', 'sql', 'statistics'],
                location='San Francisco, CA',
                salary_range='$120,000 - $150,000',
                job_type='full-time',
                experience_level='senior'
            ),
            Job(
                title='Software Engineer - Backend',
                company='StartupXYZ',
                description='Join our backend team to build scalable APIs and microservices. Experience with Python, Node.js, or Java required.',
                required_skills=['python', 'apis', 'databases', 'microservices'],
                location='Remote',
                salary_range='$100,000 - $130,000',
                job_type='full-time',
                experience_level='mid'
            ),
            Job(
                title='ML Engineer',
                company='AI Innovations',
                description='Build and deploy ML models in production. Experience with MLOps, cloud platforms, and model serving required.',
                required_skills=['python', 'machine learning', 'mlops', 'aws'],
                location='New York, NY',
                salary_range='$130,000 - $160,000',
                job_type='full-time',
                experience_level='senior'
            )
        ]
        
        for job in jobs:
            db.session.add(job)
        
        # Create learning resources
        resources = [
            LearningResource(
                title='Python for Data Science',
                description='Comprehensive course on Python programming for data science',
                resource_type='course',
                url='https://www.coursera.org/learn/python-for-data-science',
                skills_covered=['python', 'pandas', 'numpy', 'data analysis'],
                difficulty_level='beginner',
                duration='20 hours',
                provider='Coursera'
            ),
            LearningResource(
                title='Machine Learning Specialization',
                description='Learn machine learning algorithms and applications',
                resource_type='course',
                url='https://www.coursera.org/specializations/machine-learning',
                skills_covered=['machine learning', 'algorithms', 'scikit-learn'],
                difficulty_level='intermediate',
                duration='40 hours',
                provider='Coursera'
            ),
            LearningResource(
                title='React Complete Guide',
                description='Master React.js for building modern web applications',
                resource_type='course',
                url='https://www.udemy.com/course/react-the-complete-guide',
                skills_covered=['react', 'javascript', 'frontend'],
                difficulty_level='intermediate',
                duration='50 hours',
                provider='Udemy'
            ),
            LearningResource(
                title='Docker and Kubernetes Guide',
                description='Learn containerization and orchestration',
                resource_type='book',
                url='https://www.amazon.com/Docker-Kubernetes-Guide',
                skills_covered=['docker', 'kubernetes', 'devops'],
                difficulty_level='intermediate',
                duration='15 hours',
                provider='Self-paced'
            )
        ]
        
        for resource in resources:
            db.session.add(resource)
        
        # Commit all changes
        db.session.commit()
        print("Database seeded successfully!")
        print(f"Created {len(roles)} career roles")
        print(f"Created {len(jobs)} jobs")
        print(f"Created {len(resources)} learning resources")

if __name__ == '__main__':
    seed_data()

