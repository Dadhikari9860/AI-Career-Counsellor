"""
ML Inference Service - Loads trained models and provides recommendations
"""

import numpy as np
import joblib
import json
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add ml directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'ml'))

from ml.training.train_content_based import ContentBasedRecommender
from ml.training.train_collaborative_filtering import CollaborativeFilteringModel
from ml.training.train_classifier import CareerRoleClassifier
from ml.training.train_chatbot_intent import ChatbotIntentClassifier

class MLService:
    """Main ML service for inference"""
    
    def __init__(self, models_dir=None):
        if models_dir is None:
            # Default to backend/ml/models
            backend_dir = Path(__file__).parent.parent.parent
            self.models_dir = backend_dir / 'ml' / 'models'
        else:
            self.models_dir = Path(models_dir)
        self.content_based = None
        self.collaborative = None
        self.classifier = None
        self.intent_classifier = None
        self.models_loaded = False
    
    def load_models(self):
        """Load all trained models"""
        if self.models_loaded:
            return
        
        print("Loading ML models...")
        
        try:
            # Load content-based model
            metadata_path = self.models_dir / 'content_based_metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                self.content_based = ContentBasedRecommender(use_sbert=metadata.get('use_sbert', False))
                
                if not metadata.get('use_sbert', False):
                    self.content_based.tfidf_vectorizer = joblib.load(self.models_dir / 'tfidf_vectorizer.joblib')
                
                self.content_based.user_vectors = np.load(self.models_dir / 'user_vectors.npy')
                self.content_based.job_vectors = np.load(self.models_dir / 'job_vectors.npy')
                self.content_based.role_vectors = np.load(self.models_dir / 'role_vectors.npy')
                self.content_based.user_ids = np.load(self.models_dir / 'user_ids.npy')
                self.content_based.job_ids = np.load(self.models_dir / 'job_ids.npy')
                self.content_based.role_ids = np.load(self.models_dir / 'role_ids.npy')
                
                print("Content-based model loaded")
        except Exception as e:
            print(f"Warning: Could not load content-based model: {e}")
        
        try:
            # Load collaborative filtering model
            metadata_path = self.models_dir / 'svd_metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                self.collaborative = CollaborativeFilteringModel(
                    n_components=metadata.get('n_components', 50),
                    use_surprise=metadata.get('use_surprise', False)
                )
                self.collaborative.model = joblib.load(self.models_dir / 'svd_model.joblib')
                
                if not metadata.get('use_surprise', False):
                    self.collaborative.scaler = joblib.load(self.models_dir / 'svd_scaler.joblib')
                    self.collaborative.interaction_matrix = np.load(self.models_dir / 'interaction_matrix.npy')
                
                with open(self.models_dir / 'svd_user_mapping.json', 'r') as f:
                    self.collaborative.user_mapping = {int(k): v for k, v in json.load(f).items()}
                
                with open(self.models_dir / 'svd_item_mapping.json', 'r') as f:
                    self.collaborative.item_mapping = {int(k): v for k, v in json.load(f).items()}
                
                self.collaborative.is_trained = True
                print("Collaborative filtering model loaded")
        except Exception as e:
            print(f"Warning: Could not load collaborative filtering model: {e}")
        
        try:
            # Load classifier
            metadata_path = self.models_dir / 'classifier_metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                self.classifier = CareerRoleClassifier(
                    model_type=metadata.get('model_type', 'random_forest'),
                    n_estimators=metadata.get('n_estimators', 100),
                    max_depth=metadata.get('max_depth', 20)
                )
                self.classifier.model = joblib.load(self.models_dir / 'career_classifier.joblib')
                self.classifier.label_encoder = joblib.load(self.models_dir / 'label_encoder.joblib')
                
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    self.classifier.feature_names = metadata.get('feature_names', [])
                
                self.classifier.is_trained = True
                print("Classifier loaded")
        except Exception as e:
            print(f"Warning: Could not load classifier: {e}")
        
        try:
            # Load intent classifier
            metadata_path = self.models_dir / 'intent_metadata.json'
            if metadata_path.exists():
                self.intent_classifier = ChatbotIntentClassifier()
                self.intent_classifier.model = joblib.load(self.models_dir / 'intent_classifier.joblib')
                self.intent_classifier.vectorizer = joblib.load(self.models_dir / 'intent_vectorizer.joblib')
                
                with open(self.models_dir / 'intent_label_encoder.json', 'r') as f:
                    self.intent_classifier.label_encoder = json.load(f)
                
                with open(self.models_dir / 'intent_reverse_encoder.json', 'r') as f:
                    self.intent_classifier.reverse_label_encoder = {int(k): v for k, v in json.load(f).items()}
                
                self.intent_classifier.is_trained = True
                print("Intent classifier loaded")
        except Exception as e:
            print(f"Warning: Could not load intent classifier: {e}")
        
        self.models_loaded = True
        print("ML models loading complete")
    
    def get_hybrid_recommendations(self, user_features: Dict, top_k: int = 10) -> Dict:
        """Get hybrid recommendations combining all models"""
        if not self.models_loaded:
            self.load_models()
        
        results = {
            'roles': [],
            'jobs': [],
            'resources': []
        }
        
        # Content-based recommendations
        if self.content_based:
            try:
                user_vector = self.content_based.get_user_vector(user_features)
                
                # Get role recommendations
                role_recs = self.content_based.recommend_roles(user_vector, top_k=top_k)
                for rec in role_recs:
                    rec['score'] = rec['similarity_score']
                    rec['method'] = 'content_based'
                    results['roles'].append(rec)
                
                # Get job recommendations
                job_recs = self.content_based.recommend_jobs(user_vector, top_k=top_k)
                for rec in job_recs:
                    rec['score'] = rec['similarity_score']
                    rec['method'] = 'content_based'
                    results['jobs'].append(rec)
            except Exception as e:
                print(f"Error in content-based recommendations: {e}")
        
        # Classifier predictions
        if self.classifier:
            try:
                classifier_results = self.classifier.predict(user_features)
                for result in classifier_results:
                    results['roles'].append({
                        'role': result['role'],
                        'score': result['probability'],
                        'method': 'classifier'
                    })
            except Exception as e:
                print(f"Error in classifier predictions: {e}")
        
        # Collaborative filtering (if user_id available)
        if self.collaborative and 'user_id' in user_features:
            try:
                user_id = user_features['user_id']
                # Get all item IDs (would need to be passed or loaded)
                # For now, skip collaborative filtering if item list not available
                pass
            except Exception as e:
                print(f"Error in collaborative filtering: {e}")
        
        # Combine and rank by hybrid score
        # Simple weighted combination
        for role in results['roles']:
            if role['method'] == 'content_based':
                role['hybrid_score'] = role['score'] * 0.4
            elif role['method'] == 'classifier':
                role['hybrid_score'] = role['score'] * 0.6
        
        # Sort by hybrid score
        results['roles'].sort(key=lambda x: x.get('hybrid_score', x.get('score', 0)), reverse=True)
        results['jobs'].sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return results
    
    def analyze_skill_gap(self, user_skills: List[str], target_role_skills: List[str]) -> Dict:
        """Analyze skill gap between user and target role"""
        user_skills_lower = [s.lower() for s in user_skills]
        target_skills_lower = [s.lower() for s in target_role_skills]
        
        # Skills user has
        matching_skills = [s for s in target_skills_lower if any(us in s or s in us for us in user_skills_lower)]
        
        # Missing skills
        missing_skills = [s for s in target_skills_lower if not any(us in s or s in us for us in user_skills_lower)]
        
        # Calculate gap percentage
        if len(target_skills_lower) > 0:
            gap_percentage = (len(missing_skills) / len(target_skills_lower)) * 100
        else:
            gap_percentage = 0
        
        return {
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'gap_percentage': round(gap_percentage, 2),
            'match_percentage': round(100 - gap_percentage, 2)
        }
    
    def classify_intent(self, message: str) -> Dict:
        """Classify chatbot intent"""
        if not self.models_loaded:
            self.load_models()
        
        if not self.intent_classifier:
            return {
                'intent': 'general_info',
                'confidence': 0.5,
                'top_intents': []
            }
        
        try:
            return self.intent_classifier.predict(message)
        except Exception as e:
            print(f"Error classifying intent: {e}")
            return {
                'intent': 'general_info',
                'confidence': 0.5,
                'top_intents': []
            }
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance from classifier"""
        if not self.models_loaded:
            self.load_models()
        
        if not self.classifier:
            return {}
        
        try:
            return self.classifier.get_feature_importance()
        except Exception as e:
            print(f"Error getting feature importance: {e}")
            return {}

# Global ML service instance
ml_service = MLService()

