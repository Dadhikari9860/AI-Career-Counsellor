"""
Data preprocessing scripts for real datasets.
This script handles downloading, cleaning, and preparing datasets for ML training.
"""

import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
import re

class DataPreprocessor:
    """Preprocess datasets for career guidance system"""
    
    def __init__(self, raw_data_dir='data/raw', processed_data_dir='data/processed'):
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    def preprocess_resume_dataset(self, filepath):
        """
        Preprocess resume/user profile dataset
        Expected columns: skills, experience, education, role, etc.
        """
        print("Preprocessing resume dataset...")
        df = pd.read_csv(filepath)
        
        # Clean and standardize skills
        if 'skills' in df.columns:
            df['skills_cleaned'] = df['skills'].apply(self._clean_skills)
        else:
            # If skills are in separate columns, combine them
            skill_cols = [col for col in df.columns if 'skill' in col.lower()]
            if skill_cols:
                df['skills_cleaned'] = df[skill_cols].apply(
                    lambda row: self._clean_skills(' '.join(row.astype(str))), axis=1
                )
        
        # Extract experience years
        if 'experience' in df.columns:
            df['experience_years'] = df['experience'].apply(self._extract_years)
        
        # Standardize role titles
        if 'role' in df.columns or 'job_title' in df.columns:
            role_col = 'role' if 'role' in df.columns else 'job_title'
            df['role_normalized'] = df[role_col].apply(self._normalize_role)
        
        # Save processed data
        output_path = self.processed_data_dir / 'resumes_processed.csv'
        df.to_csv(output_path, index=False)
        print(f"Saved processed resume data to {output_path}")
        return df
    
    def preprocess_job_postings(self, filepath):
        """
        Preprocess job postings dataset
        Expected columns: title, description, required_skills, location, etc.
        """
        print("Preprocessing job postings dataset...")
        df = pd.read_csv(filepath)
        
        # Clean job descriptions
        if 'description' in df.columns:
            df['description_cleaned'] = df['description'].apply(self._clean_text)
        
        # Extract and clean required skills
        if 'required_skills' in df.columns or 'skills' in df.columns:
            skill_col = 'required_skills' if 'required_skills' in df.columns else 'skills'
            df['skills_cleaned'] = df[skill_col].apply(self._clean_skills)
        elif 'description' in df.columns:
            # Extract skills from description
            df['skills_cleaned'] = df['description'].apply(self._extract_skills_from_text)
        
        # Normalize job titles
        if 'title' in df.columns or 'job_title' in df.columns:
            title_col = 'title' if 'title' in df.columns else 'job_title'
            df['title_normalized'] = df[title_col].apply(self._normalize_role)
        
        # Extract experience level from description
        if 'description' in df.columns:
            df['experience_level'] = df['description'].apply(self._extract_experience_level)
        
        output_path = self.processed_data_dir / 'jobs_processed.csv'
        df.to_csv(output_path, index=False)
        print(f"Saved processed job data to {output_path}")
        return df
    
    def preprocess_interactions(self, filepath):
        """
        Preprocess user-job/career interactions dataset
        Expected columns: user_id, item_id, rating/interaction, etc.
        """
        print("Preprocessing interactions dataset...")
        df = pd.read_csv(filepath)
        
        # Normalize user and item IDs
        if 'user_id' in df.columns:
            df['user_id'] = pd.Categorical(df['user_id']).codes
        if 'item_id' in df.columns or 'job_id' in df.columns:
            item_col = 'item_id' if 'item_id' in df.columns else 'job_id'
            df['item_id'] = pd.Categorical(df[item_col]).codes
        
        # Normalize ratings/interactions
        if 'rating' in df.columns:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            df['rating'] = df['rating'].fillna(df['rating'].median())
        elif 'interaction' in df.columns:
            # Convert interaction types to numeric ratings
            interaction_map = {'click': 1, 'save': 2, 'apply': 3, 'like': 2, 'dislike': 0}
            df['rating'] = df['interaction'].map(interaction_map).fillna(1)
        else:
            # Create default ratings
            df['rating'] = 1
        
        output_path = self.processed_data_dir / 'interactions_processed.csv'
        df.to_csv(output_path, index=False)
        print(f"Saved processed interactions data to {output_path}")
        return df
    
    def create_merged_dataset(self):
        """Create a merged dataset combining all sources"""
        print("Creating merged dataset...")
        
        resumes_path = self.processed_data_dir / 'resumes_processed.csv'
        jobs_path = self.processed_data_dir / 'jobs_processed.csv'
        interactions_path = self.processed_data_dir / 'interactions_processed.csv'
        
        merged_data = {}
        
        if resumes_path.exists():
            merged_data['resumes'] = pd.read_csv(resumes_path)
        if jobs_path.exists():
            merged_data['jobs'] = pd.read_csv(jobs_path)
        if interactions_path.exists():
            merged_data['interactions'] = pd.read_csv(interactions_path)
        
        # Save merged data summary
        summary = {
            'resumes_count': len(merged_data.get('resumes', [])),
            'jobs_count': len(merged_data.get('jobs', [])),
            'interactions_count': len(merged_data.get('interactions', []))
        }
        
        summary_path = self.processed_data_dir / 'dataset_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Dataset summary saved to {summary_path}")
        return merged_data
    
    def _clean_skills(self, skills_str):
        """Clean and normalize skills string"""
        if pd.isna(skills_str):
            return []
        
        # Convert to string and split
        skills_str = str(skills_str).lower()
        # Handle different separators
        skills = re.split(r'[,;|]|\s+and\s+', skills_str)
        
        # Clean each skill
        cleaned = []
        for skill in skills:
            skill = skill.strip()
            # Remove common prefixes/suffixes
            skill = re.sub(r'^(proficient in|expert in|knowledge of|experience with)\s+', '', skill)
            skill = skill.strip()
            if len(skill) > 2:  # Filter out very short strings
                cleaned.append(skill)
        
        return list(set(cleaned))  # Remove duplicates
    
    def _clean_text(self, text):
        """Clean text description"""
        if pd.isna(text):
            return ""
        text = str(text)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_years(self, exp_str):
        """Extract years of experience from string"""
        if pd.isna(exp_str):
            return 0
        exp_str = str(exp_str).lower()
        # Look for patterns like "5 years", "5+ years", etc.
        match = re.search(r'(\d+)\s*\+?\s*years?', exp_str)
        if match:
            return int(match.group(1))
        return 0
    
    def _normalize_role(self, role):
        """Normalize role/job title"""
        if pd.isna(role):
            return ""
        role = str(role).lower().strip()
        # Common normalizations
        role = re.sub(r'\s+', ' ', role)
        return role.title()
    
    def _extract_skills_from_text(self, text):
        """Extract skills mentioned in text"""
        if pd.isna(text):
            return []
        
        # Common tech skills to look for
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
            'aws', 'docker', 'kubernetes', 'git', 'linux', 'html', 'css',
            'machine learning', 'data science', 'tensorflow', 'pytorch',
            'agile', 'scrum', 'rest api', 'graphql', 'microservices'
        ]
        
        text_lower = str(text).lower()
        found_skills = [skill for skill in common_skills if skill in text_lower]
        return found_skills
    
    def _extract_experience_level(self, text):
        """Extract experience level from job description"""
        if pd.isna(text):
            return "mid"
        
        text_lower = str(text).lower()
        if any(word in text_lower for word in ['entry', 'junior', 'graduate', 'intern']):
            return "entry"
        elif any(word in text_lower for word in ['senior', 'lead', 'principal', 'architect']):
            return "senior"
        else:
            return "mid"

def main():
    """Main preprocessing function"""
    preprocessor = DataPreprocessor()
    
    # Check for raw data files
    raw_dir = Path('data/raw')
    
    # Process resume dataset if available
    resume_files = list(raw_dir.glob('*resume*.csv')) + list(raw_dir.glob('*profile*.csv'))
    if resume_files:
        preprocessor.preprocess_resume_dataset(resume_files[0])
    
    # Process job postings if available
    job_files = list(raw_dir.glob('*job*.csv')) + list(raw_dir.glob('*posting*.csv'))
    if job_files:
        preprocessor.preprocess_job_postings(job_files[0])
    
    # Process interactions if available
    interaction_files = list(raw_dir.glob('*interaction*.csv')) + list(raw_dir.glob('*rating*.csv'))
    if interaction_files:
        preprocessor.preprocess_interactions(interaction_files[0])
    
    # Create merged dataset
    preprocessor.create_merged_dataset()
    
    print("Data preprocessing complete!")

if __name__ == '__main__':
    main()

