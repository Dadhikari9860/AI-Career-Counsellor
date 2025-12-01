"""
Train content-based recommendation model using TF-IDF and optionally Sentence-BERT
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_BERT_AVAILABLE = True
except ImportError:
    SENTENCE_BERT_AVAILABLE = False
    # This is fine - TF-IDF works well without Sentence-BERT
    pass

class ContentBasedRecommender:
    """Content-based recommendation using TF-IDF and/or Sentence-BERT"""
    
    def __init__(self, use_sbert=False):
        self.use_sbert = use_sbert and SENTENCE_BERT_AVAILABLE
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2,
            max_df=0.95
        )
        self.sbert_model = None
        if self.use_sbert:
            print("Loading Sentence-BERT model...")
            self.sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.user_vectors = None
        self.job_vectors = None
        self.role_vectors = None
        self.user_ids = None
        self.job_ids = None
        self.role_ids = None
    
    def prepare_user_features(self, users_df, fit_vectorizer=False):
        """Prepare user feature vectors"""
        print("Preparing user features...")
        
        # Combine user features into text
        user_texts = []
        user_ids = []
        
        for _, user in users_df.iterrows():
            features = []
            
            # Add skills
            if 'skills_cleaned' in user and isinstance(user['skills_cleaned'], list):
                features.extend(user['skills_cleaned'])
            elif 'skills' in user:
                skills = str(user['skills']).lower()
                features.extend(skills.split())
            
            # Add experience
            if 'experience_years' in user:
                features.append(f"{int(user['experience_years'])} years experience")
            
            # Add current role
            if 'current_role' in user and pd.notna(user['current_role']):
                features.append(str(user['current_role']).lower())
            
            # Add interests
            if 'interests' in user and isinstance(user['interests'], list):
                features.extend([str(i).lower() for i in user['interests']])
            
            user_text = ' '.join(features)
            user_texts.append(user_text)
            user_ids.append(user.get('id', len(user_ids)))
        
        # Vectorize
        if self.use_sbert:
            self.user_vectors = np.array(self.sbert_model.encode(user_texts))
        else:
            if fit_vectorizer:
                # Fit vectorizer on user data (first time)
                self.user_vectors = self.tfidf_vectorizer.fit_transform(user_texts).toarray()
            else:
                # Transform using already-fitted vectorizer
                self.user_vectors = self.tfidf_vectorizer.transform(user_texts).toarray()
        
        self.user_ids = np.array(user_ids)
        print(f"Created {len(user_texts)} user vectors")
    
    def prepare_job_features(self, jobs_df):
        """Prepare job feature vectors"""
        print("Preparing job features...")
        
        job_texts = []
        job_ids = []
        
        for _, job in jobs_df.iterrows():
            features = []
            
            # Add title
            if 'title' in job and pd.notna(job['title']):
                features.append(str(job['title']).lower())
            
            # Add description
            if 'description_cleaned' in job and pd.notna(job['description_cleaned']):
                features.append(str(job['description_cleaned']).lower())
            elif 'description' in job and pd.notna(job['description']):
                features.append(str(job['description']).lower())
            
            # Add required skills
            if 'skills_cleaned' in job:
                if isinstance(job['skills_cleaned'], list):
                    features.extend([str(s).lower() for s in job['skills_cleaned']])
                else:
                    features.append(str(job['skills_cleaned']).lower())
            
            job_text = ' '.join(features)
            job_texts.append(job_text)
            job_ids.append(job.get('id', len(job_ids)))
        
        # Vectorize
        if self.use_sbert:
            self.job_vectors = np.array(self.sbert_model.encode(job_texts))
        else:
            # Always transform (vectorizer should be fitted on combined corpus first)
            # This prevents data leakage where vocabulary is determined by one data type
            if hasattr(self.tfidf_vectorizer, 'vocabulary_') and len(self.tfidf_vectorizer.vocabulary_) > 0:
                self.job_vectors = self.tfidf_vectorizer.transform(job_texts).toarray()
            else:
                # If vectorizer not fitted yet, fit on job data (fallback, but not ideal)
                print("Warning: Fitting vectorizer on job data only. Consider fitting on combined corpus.")
                self.job_vectors = self.tfidf_vectorizer.fit_transform(job_texts).toarray()
        
        self.job_ids = np.array(job_ids)
        print(f"Created {len(job_texts)} job vectors")
    
    def prepare_role_features(self, roles_df):
        """Prepare career role feature vectors"""
        print("Preparing role features...")
        
        role_texts = []
        role_ids = []
        
        for _, role in roles_df.iterrows():
            features = []
            
            # Add title
            if 'title' in role and pd.notna(role['title']):
                features.append(str(role['title']).lower())
            
            # Add description
            if 'description' in role and pd.notna(role['description']):
                features.append(str(role['description']).lower())
            
            # Add required skills
            if 'required_skills' in role:
                if isinstance(role['required_skills'], list):
                    features.extend([str(s).lower() for s in role['required_skills']])
                else:
                    features.append(str(role['required_skills']).lower())
            
            role_text = ' '.join(features)
            role_texts.append(role_text)
            role_ids.append(role.get('id', len(role_ids)))
        
        # Vectorize
        if self.use_sbert:
            self.role_vectors = np.array(self.sbert_model.encode(role_texts))
        else:
            # Always transform (vectorizer should be fitted on combined corpus first)
            if hasattr(self.tfidf_vectorizer, 'vocabulary_') and len(self.tfidf_vectorizer.vocabulary_) > 0:
                self.role_vectors = self.tfidf_vectorizer.transform(role_texts).toarray()
            else:
                # If vectorizer not fitted yet, fit on role data (fallback, but not ideal)
                print("Warning: Fitting vectorizer on role data only. Consider fitting on combined corpus.")
                self.role_vectors = self.tfidf_vectorizer.fit_transform(role_texts).toarray()
        
        self.role_ids = np.array(role_ids)
        print(f"Created {len(role_texts)} role vectors")
    
    def recommend_jobs(self, user_vector, top_k=10):
        """Recommend jobs for a user"""
        if self.job_vectors is None:
            return []
        
        similarities = cosine_similarity([user_vector], self.job_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        recommendations = []
        for idx in top_indices:
            recommendations.append({
                'job_id': int(self.job_ids[idx]),
                'similarity_score': float(similarities[idx])
            })
        
        return recommendations
    
    def recommend_roles(self, user_vector, top_k=10):
        """Recommend roles for a user"""
        if self.role_vectors is None:
            return []
        
        similarities = cosine_similarity([user_vector], self.role_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        recommendations = []
        for idx in top_indices:
            recommendations.append({
                'role_id': int(self.role_ids[idx]),
                'similarity_score': float(similarities[idx])
            })
        
        return recommendations
    
    def get_user_vector(self, user_features):
        """Get vector for a new user"""
        # Prepare text from user features
        features = []
        if 'skills' in user_features:
            if isinstance(user_features['skills'], list):
                features.extend([str(s).lower() for s in user_features['skills']])
            else:
                features.append(str(user_features['skills']).lower())
        
        if 'experience_years' in user_features:
            features.append(f"{int(user_features['experience_years'])} years experience")
        
        if 'current_role' in user_features:
            features.append(str(user_features['current_role']).lower())
        
        user_text = ' '.join(features)
        
        if self.use_sbert:
            return self.sbert_model.encode([user_text])[0]
        else:
            return self.tfidf_vectorizer.transform([user_text]).toarray()[0]
    
    def save(self, model_dir='ml/models'):
        """Save the model"""
        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Save vectorizer
        if not self.use_sbert:
            joblib.dump(self.tfidf_vectorizer, model_path / 'tfidf_vectorizer.joblib')
        
        # Save vectors and IDs
        np.save(model_path / 'user_vectors.npy', self.user_vectors)
        np.save(model_path / 'job_vectors.npy', self.job_vectors)
        np.save(model_path / 'role_vectors.npy', self.role_vectors)
        
        np.save(model_path / 'user_ids.npy', self.user_ids)
        np.save(model_path / 'job_ids.npy', self.job_ids)
        np.save(model_path / 'role_ids.npy', self.role_ids)
        
        # Save metadata
        metadata = {
            'use_sbert': self.use_sbert,
            'num_users': len(self.user_ids) if self.user_ids is not None else 0,
            'num_jobs': len(self.job_ids) if self.job_ids is not None else 0,
            'num_roles': len(self.role_ids) if self.role_ids is not None else 0
        }
        
        with open(model_path / 'content_based_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to {model_path}")

def main():
    """Train content-based model"""
    print("Training content-based recommendation model...")
    
    data_dir = Path('data/processed')
    
    # Load processed data
    users_df = pd.read_csv(data_dir / 'resumes_processed.csv') if (data_dir / 'resumes_processed.csv').exists() else None
    jobs_df = pd.read_csv(data_dir / 'jobs_processed.csv') if (data_dir / 'jobs_processed.csv').exists() else None
    
    # Create sample data if files don't exist (for testing)
    if users_df is None or len(users_df) == 0:
        print("No user data found, creating sample data...")
        users_df = pd.DataFrame({
            'id': range(100),
            'skills_cleaned': [['python', 'sql', 'machine learning']] * 100,
            'experience_years': np.random.randint(0, 10, 100),
            'current_role': ['Data Scientist', 'Software Engineer', 'ML Engineer'] * 33 + ['Data Scientist']
        })
    
    if jobs_df is None or len(jobs_df) == 0:
        print("No job data found, creating sample data...")
        jobs_df = pd.DataFrame({
            'id': range(50),
            'title': ['Senior Data Scientist', 'Python Developer', 'ML Engineer'] * 16 + ['Senior Data Scientist', 'Python Developer'],
            'description': ['Looking for experienced data scientist'] * 50,
            'skills_cleaned': [['python', 'machine learning', 'sql']] * 50
        })
    
    # Create roles data
    roles_df = pd.DataFrame({
        'id': range(20),
        'title': [
            'Data Scientist', 'Software Engineer', 'ML Engineer', 'Data Analyst',
            'Backend Developer', 'Frontend Developer', 'Full Stack Developer',
            'DevOps Engineer', 'Cloud Architect', 'Product Manager',
            'UX Designer', 'Data Engineer', 'Security Engineer', 'QA Engineer',
            'Mobile Developer', 'Blockchain Developer', 'AI Researcher',
            'Business Analyst', 'Technical Writer', 'Solutions Architect'
        ],
        'description': ['Career role description'] * 20,
        'required_skills': [['python', 'sql'], ['java', 'spring'], ['python', 'tensorflow']] * 6 + [['python', 'sql'], ['java', 'spring']]
    })
    
    # Train model
    model = ContentBasedRecommender(use_sbert=False)  # Use TF-IDF for faster training
    
    # CRITICAL FIX: Fit vectorizer on ALL data combined to prevent data leakage
    # This ensures the vocabulary is determined by the entire corpus, not just one data type
    print("Fitting vectorizer on combined corpus to prevent data leakage...")
    all_texts = []
    
    # Collect all user texts
    if users_df is not None and len(users_df) > 0:
        for _, user in users_df.iterrows():
            features = []
            if 'skills_cleaned' in user and isinstance(user['skills_cleaned'], list):
                features.extend(user['skills_cleaned'])
            elif 'skills' in user:
                features.extend(str(user['skills']).lower().split())
            if 'experience_years' in user:
                features.append(f"{int(user['experience_years'])} years experience")
            if 'current_role' in user and pd.notna(user['current_role']):
                features.append(str(user['current_role']).lower())
            all_texts.append(' '.join(features))
    
    # Collect all job texts
    if jobs_df is not None and len(jobs_df) > 0:
        for _, job in jobs_df.iterrows():
            features = []
            if 'title' in job and pd.notna(job['title']):
                features.append(str(job['title']).lower())
            if 'description_cleaned' in job and pd.notna(job['description_cleaned']):
                features.append(str(job['description_cleaned']).lower())
            elif 'description' in job and pd.notna(job['description']):
                features.append(str(job['description']).lower())
            if 'skills_cleaned' in job:
                if isinstance(job['skills_cleaned'], list):
                    features.extend([str(s).lower() for s in job['skills_cleaned']])
                else:
                    features.append(str(job['skills_cleaned']).lower())
            all_texts.append(' '.join(features))
    
    # Collect all role texts
    for _, role in roles_df.iterrows():
        features = []
        if 'title' in role and pd.notna(role['title']):
            features.append(str(role['title']).lower())
        if 'description' in role and pd.notna(role['description']):
            features.append(str(role['description']).lower())
        if 'required_skills' in role:
            if isinstance(role['required_skills'], list):
                features.extend([str(s).lower() for s in role['required_skills']])
            else:
                features.append(str(role['required_skills']).lower())
        all_texts.append(' '.join(features))
    
    # Fit vectorizer on combined corpus
    if not model.use_sbert and len(all_texts) > 0:
        model.tfidf_vectorizer.fit(all_texts)
        print(f"Vectorizer fitted on {len(all_texts)} combined documents")
    
    # Now transform each data type separately using the fitted vectorizer
    if users_df is not None and len(users_df) > 0:
        model.prepare_user_features(users_df, fit_vectorizer=False)
    
    if jobs_df is not None and len(jobs_df) > 0:
        model.prepare_job_features(jobs_df)
    
    model.prepare_role_features(roles_df)
    
    # Save model
    model.save()
    
    print("Content-based model training complete!")

if __name__ == '__main__':
    main()

