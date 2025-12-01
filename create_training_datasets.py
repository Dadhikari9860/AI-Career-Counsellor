"""
Script to create training datasets for the Career Guidance System
This generates realistic sample datasets that can be used for model training
"""

import pandas as pd
import numpy as np
from pathlib import Path
import zipfile
import json

def create_resume_dataset(n_samples=1000):
    """Create resume/user profile dataset"""
    print(f"Creating resume dataset with {n_samples} samples...")
    
    roles = [
        'Data Scientist', 'Software Engineer', 'ML Engineer', 'Data Analyst',
        'Backend Developer', 'Frontend Developer', 'Full Stack Developer',
        'DevOps Engineer', 'Product Manager', 'UX Designer',
        'Data Engineer', 'Security Engineer', 'QA Engineer',
        'Mobile Developer', 'Cloud Architect', 'AI Researcher'
    ]
    
    # Role-specific skill patterns
    role_skills = {
        'Data Scientist': ['python', 'sql', 'machine learning', 'pandas', 'numpy', 'statistics', 'data science', 'scikit-learn'],
        'ML Engineer': ['python', 'machine learning', 'tensorflow', 'pytorch', 'aws', 'docker', 'kubernetes'],
        'Data Analyst': ['python', 'sql', 'pandas', 'excel', 'analytics', 'statistics', 'tableau'],
        'Software Engineer': ['java', 'spring', 'sql', 'rest api', 'microservices', 'git', 'docker'],
        'Backend Developer': ['java', 'spring', 'sql', 'rest api', 'microservices', 'postgresql', 'redis'],
        'Frontend Developer': ['javascript', 'react', 'html', 'css', 'typescript', 'node.js', 'redux'],
        'Full Stack Developer': ['javascript', 'react', 'node.js', 'sql', 'rest api', 'html', 'css', 'mongodb'],
        'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'linux', 'ci/cd', 'git', 'terraform', 'ansible'],
        'Product Manager': ['agile', 'scrum', 'product management', 'analytics', 'jira', 'confluence', 'figma'],
        'UX Designer': ['design', 'figma', 'user research', 'prototyping', 'html', 'css', 'adobe xd'],
        'Data Engineer': ['python', 'sql', 'spark', 'hadoop', 'airflow', 'aws', 'etl'],
        'Security Engineer': ['python', 'linux', 'networking', 'security', 'penetration testing', 'aws'],
        'QA Engineer': ['selenium', 'python', 'testing', 'automation', 'jira', 'test planning'],
        'Mobile Developer': ['swift', 'kotlin', 'react native', 'ios', 'android', 'firebase'],
        'Cloud Architect': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'cloud architecture'],
        'AI Researcher': ['python', 'tensorflow', 'pytorch', 'research', 'machine learning', 'deep learning', 'nlp']
    }
    
    data_rows = []
    for i in range(n_samples):
        role_idx = i % len(roles)
        role = roles[role_idx]
        
        # Get base skills for this role
        base_skills = role_skills.get(role, ['python', 'sql', 'git'])
        
        # Add some variation
        skills = base_skills.copy()
        
        # Add common skills (30% chance)
        common_skills = ['git', 'jira', 'agile', 'communication', 'problem solving', 
                        'teamwork', 'project management', 'documentation']
        if np.random.random() < 0.3:
            skills.append(np.random.choice(common_skills))
        
        # Add some cross-role skills (20% chance)
        if np.random.random() < 0.2:
            other_roles = [r for r in roles if r != role]
            other_role = np.random.choice(other_roles)
            if other_role in role_skills:
                cross_skill = np.random.choice(role_skills[other_role])
                if cross_skill not in skills:
                    skills.append(cross_skill)
        
        # Remove a random skill occasionally (10% chance)
        if np.random.random() < 0.1 and len(skills) > 3:
            skills.pop(np.random.randint(0, len(skills)))
        
        # Experience years based on role
        if 'Senior' in role or 'Lead' in role or 'Architect' in role:
            exp_years = np.random.randint(5, 15)
        elif 'Junior' in role or 'Entry' in role:
            exp_years = np.random.randint(0, 3)
        else:
            exp_years = np.random.randint(1, 8)
        
        # Education based on role
        if role in ['Data Scientist', 'ML Engineer', 'AI Researcher', 'Product Manager']:
            education = ['master'] if np.random.random() > 0.3 else ['bachelor']
        else:
            education = ['bachelor'] if np.random.random() > 0.4 else ['master']
        
        # Add PhD occasionally
        if np.random.random() < 0.05:
            education.append('phd')
        
        data_rows.append({
            'id': i,
            'skills_cleaned': skills,
            'experience_years': exp_years,
            'current_role': role,
            'target_role': role,
            'education': education
        })
    
    df = pd.DataFrame(data_rows)
    return df

def create_job_postings_dataset(n_samples=500):
    """Create job postings dataset"""
    print(f"Creating job postings dataset with {n_samples} samples...")
    
    job_titles = [
        'Senior Data Scientist', 'Data Scientist', 'Junior Data Scientist',
        'Senior Software Engineer', 'Software Engineer', 'Junior Software Engineer',
        'ML Engineer', 'Senior ML Engineer',
        'Data Analyst', 'Senior Data Analyst',
        'Backend Developer', 'Senior Backend Developer',
        'Frontend Developer', 'Senior Frontend Developer',
        'Full Stack Developer', 'Senior Full Stack Developer',
        'DevOps Engineer', 'Senior DevOps Engineer',
        'Product Manager', 'Senior Product Manager',
        'UX Designer', 'Senior UX Designer',
        'Data Engineer', 'Cloud Architect', 'Security Engineer'
    ]
    
    job_descriptions = {
        'Data Scientist': 'We are looking for an experienced Data Scientist to analyze complex datasets and build predictive models. You will work with cross-functional teams to identify business opportunities and provide data-driven insights.',
        'Software Engineer': 'Join our engineering team to build scalable software solutions. You will design, develop, and maintain high-quality applications using modern technologies and best practices.',
        'ML Engineer': 'We seek a Machine Learning Engineer to develop and deploy ML models in production. You will work on end-to-end ML pipelines and collaborate with data scientists and engineers.',
        'Data Analyst': 'Looking for a Data Analyst to transform raw data into actionable insights. You will create reports, dashboards, and help stakeholders make data-driven decisions.',
        'Backend Developer': 'Seeking a Backend Developer to build robust server-side applications. You will work with databases, APIs, and microservices architecture.',
        'Frontend Developer': 'Join our frontend team to create beautiful and responsive user interfaces. You will work with modern frameworks and ensure excellent user experience.',
        'Full Stack Developer': 'We need a Full Stack Developer who can work on both frontend and backend. You will build complete web applications from database to UI.',
        'DevOps Engineer': 'Looking for a DevOps Engineer to manage our infrastructure and CI/CD pipelines. You will ensure system reliability and scalability.',
        'Product Manager': 'Seeking a Product Manager to drive product strategy and execution. You will work with engineering, design, and business teams to deliver great products.',
        'UX Designer': 'Join our design team to create intuitive user experiences. You will conduct user research, create wireframes, and design beautiful interfaces.'
    }
    
    # Job-specific required skills
    job_skills = {
        'Data Scientist': ['python', 'sql', 'machine learning', 'pandas', 'numpy', 'statistics'],
        'Software Engineer': ['java', 'spring', 'sql', 'rest api', 'microservices'],
        'ML Engineer': ['python', 'machine learning', 'tensorflow', 'pytorch', 'aws'],
        'Data Analyst': ['python', 'sql', 'pandas', 'excel', 'analytics'],
        'Backend Developer': ['java', 'spring', 'sql', 'rest api', 'postgresql'],
        'Frontend Developer': ['javascript', 'react', 'html', 'css', 'typescript'],
        'Full Stack Developer': ['javascript', 'react', 'node.js', 'sql', 'rest api'],
        'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'linux', 'ci/cd'],
        'Product Manager': ['agile', 'scrum', 'product management', 'analytics'],
        'UX Designer': ['design', 'figma', 'user research', 'prototyping']
    }
    
    data_rows = []
    for i in range(n_samples):
        title = np.random.choice(job_titles)
        
        # Extract base role from title
        base_role = title.replace('Senior ', '').replace('Junior ', '')
        for key in job_skills.keys():
            if key in base_role:
                base_role = key
                break
        
        # Get description
        description = job_descriptions.get(base_role, 'We are looking for a talented professional to join our team.')
        
        # Get required skills
        required_skills = job_skills.get(base_role, ['python', 'sql', 'git']).copy()
        
        # Add some variation
        if np.random.random() < 0.3:
            required_skills.append(np.random.choice(['git', 'jira', 'agile', 'communication']))
        
        data_rows.append({
            'id': i,
            'title': title,
            'description': description,
            'description_cleaned': description.lower(),
            'skills_cleaned': required_skills,
            'location': np.random.choice(['Remote', 'New York', 'San Francisco', 'London', 'Bangalore', 'Hybrid']),
            'salary_range': f"${np.random.randint(80, 200)}k - ${np.random.randint(200, 350)}k"
        })
    
    df = pd.DataFrame(data_rows)
    return df

def create_interactions_dataset(n_users=200, n_jobs=500, n_interactions=2000):
    """Create user-job interactions dataset"""
    print(f"Creating interactions dataset with {n_interactions} interactions...")
    
    # Create interactions with some patterns
    interactions = []
    user_ids = list(range(n_users))
    job_ids = list(range(n_jobs))
    
    for _ in range(n_interactions):
        user_id = np.random.choice(user_ids)
        job_id = np.random.choice(job_ids)
        
        # Ratings tend to be positive (3-5) with some variation
        if np.random.random() < 0.7:
            rating = np.random.choice([3, 4, 5], p=[0.2, 0.4, 0.4])
        else:
            rating = np.random.choice([1, 2, 3], p=[0.3, 0.4, 0.3])
        
        interactions.append({
            'user_id': user_id,
            'item_id': job_id,
            'rating': rating
        })
    
    df = pd.DataFrame(interactions)
    # Remove duplicates
    df = df.drop_duplicates(subset=['user_id', 'item_id'])
    
    return df

def main():
    """Create all datasets and save them"""
    print("="*70)
    print("CREATING TRAINING DATASETS")
    print("="*70)
    
    # Create processed data directory
    processed_dir = Path('data/processed')
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Create datasets
    print("\n[1/3] Creating resume dataset...")
    resumes_df = create_resume_dataset(n_samples=1000)
    resumes_path = processed_dir / 'resumes_processed.csv'
    resumes_df.to_csv(resumes_path, index=False)
    print(f"✅ Saved: {resumes_path} ({len(resumes_df)} rows)")
    
    print("\n[2/3] Creating job postings dataset...")
    jobs_df = create_job_postings_dataset(n_samples=500)
    jobs_path = processed_dir / 'jobs_processed.csv'
    jobs_df.to_csv(jobs_path, index=False)
    print(f"✅ Saved: {jobs_path} ({len(jobs_df)} rows)")
    
    print("\n[3/3] Creating interactions dataset...")
    interactions_df = create_interactions_dataset(n_users=200, n_jobs=500, n_interactions=2000)
    interactions_path = processed_dir / 'interactions_processed.csv'
    interactions_df.to_csv(interactions_path, index=False)
    print(f"✅ Saved: {interactions_path} ({len(interactions_df)} rows)")
    
    # Create zip file
    print("\n[4/4] Creating zip file...")
    zip_path = Path('training_datasets.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(resumes_path, 'resumes_processed.csv')
        zipf.write(jobs_path, 'jobs_processed.csv')
        zipf.write(interactions_path, 'interactions_processed.csv')
    
    zip_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"✅ Created: {zip_path} ({zip_size:.2f} MB)")
    
    # Create dataset info
    info = {
        'resumes_count': len(resumes_df),
        'jobs_count': len(jobs_df),
        'interactions_count': len(interactions_df),
        'description': 'Training datasets for Career Guidance System ML models'
    }
    
    info_path = processed_dir / 'dataset_info.json'
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=2)
    
    print("\n" + "="*70)
    print("✅ All datasets created successfully!")
    print("="*70)
    print(f"\nDataset Summary:")
    print(f"  - Resumes: {len(resumes_df)} samples")
    print(f"  - Jobs: {len(jobs_df)} samples")
    print(f"  - Interactions: {len(interactions_df)} samples")
    print(f"\n📦 Zip file: {zip_path} ({zip_size:.2f} MB)")

if __name__ == '__main__':
    main()



