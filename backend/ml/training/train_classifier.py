"""
Train supervised classifier (Random Forest / Decision Tree) for career role prediction
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import json

class CareerRoleClassifier:
    """Supervised classifier for predicting suitable career roles"""
    
    def __init__(self, model_type='random_forest', n_estimators=200, max_depth=15, min_samples_split=10):
        self.model_type = model_type
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        
        if model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=5,  # Increased to prevent overfitting
                random_state=42,
                n_jobs=-1,
                class_weight='balanced',  # Handle class imbalance
                max_features='sqrt',  # Prevent overfitting
                bootstrap=True,
                oob_score=True,  # Out-of-bag score for validation
                max_samples=0.8  # Use 80% of samples per tree to reduce overfitting
            )
        else:
            self.model = DecisionTreeClassifier(
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=42,
                class_weight='balanced'
            )
        
        self.label_encoder = LabelEncoder()
        self.skill_binarizer = MultiLabelBinarizer()
        self.feature_names = []
        self.is_trained = False
    
    def prepare_features(self, users_df, roles_df=None):
        """Prepare features from user data"""
        print("Preparing features...")
        
        features_list = []
        labels_list = []
        
        # Extract features from users
        for _, user in users_df.iterrows():
            feature_dict = {}
            
            # Experience years
            feature_dict['experience_years'] = user.get('experience_years', 0)
            
            # Skills (one-hot encoded)
            skills = user.get('skills_cleaned', [])
            if isinstance(skills, str):
                # Try to parse if it's a string representation of list
                import ast
                try:
                    skills = ast.literal_eval(skills)
                except:
                    skills = [skills]
            
            if not isinstance(skills, list):
                skills = []
            
            # Create binary features for common skills (expanded list)
            common_skills = [
                'python', 'java', 'javascript', 'sql', 'react', 'node.js',
                'machine learning', 'data science', 'aws', 'docker',
                'git', 'linux', 'html', 'css', 'mongodb', 'tensorflow',
                'pytorch', 'agile', 'scrum', 'rest api', 'spring', 'pandas',
                'numpy', 'statistics', 'microservices', 'kubernetes', 'ci/cd',
                'typescript', 'design', 'figma', 'user research', 'prototyping',
                'product management', 'analytics', 'jira', 'confluence'
            ]
            
            for skill in common_skills:
                # Check if skill exists in user's skills
                skill_found = any(
                    skill.lower() in str(s).lower() or str(s).lower() in skill.lower()
                    for s in skills
                )
                feature_dict[f'skill_{skill}'] = 1 if skill_found else 0
            
            # Count of skills
            feature_dict['num_skills'] = len(skills)
            
            # Skill categories
            data_skills = ['python', 'sql', 'machine learning', 'data science', 'pandas', 'numpy', 'statistics']
            web_skills = ['javascript', 'react', 'node.js', 'html', 'css', 'typescript']
            backend_skills = ['java', 'spring', 'sql', 'rest api', 'microservices']
            devops_skills = ['docker', 'kubernetes', 'aws', 'linux', 'ci/cd']
            design_skills = ['design', 'figma', 'user research', 'prototyping']
            pm_skills = ['agile', 'scrum', 'product management', 'analytics', 'jira']
            
            feature_dict['data_skill_count'] = sum(1 for s in skills if any(ds in str(s).lower() for ds in data_skills))
            feature_dict['web_skill_count'] = sum(1 for s in skills if any(ws in str(s).lower() for ws in web_skills))
            feature_dict['backend_skill_count'] = sum(1 for s in skills if any(bs in str(s).lower() for bs in backend_skills))
            feature_dict['devops_skill_count'] = sum(1 for s in skills if any(ds in str(s).lower() for ds in devops_skills))
            feature_dict['design_skill_count'] = sum(1 for s in skills if any(ds in str(s).lower() for ds in design_skills))
            feature_dict['pm_skill_count'] = sum(1 for s in skills if any(ps in str(s).lower() for ps in pm_skills))
            
            # Education level (if available)
            education = user.get('education', [])
            if isinstance(education, str):
                try:
                    import ast
                    education = ast.literal_eval(education)
                except:
                    education = []
            
            feature_dict['has_bachelor'] = 1 if any('bachelor' in str(e).lower() for e in education) else 0
            feature_dict['has_master'] = 1 if any('master' in str(e).lower() for e in education) else 0
            feature_dict['has_phd'] = 1 if any('phd' in str(e).lower() or 'doctorate' in str(e).lower() for e in education) else 0
            
            features_list.append(feature_dict)
            
            # Label (target role or current role)
            if 'target_role' in user and pd.notna(user['target_role']):
                labels_list.append(str(user['target_role']))
            elif 'role_normalized' in user and pd.notna(user['role_normalized']):
                labels_list.append(str(user['role_normalized']))
            elif 'current_role' in user and pd.notna(user['current_role']):
                labels_list.append(str(user['current_role']))
            else:
                labels_list.append('Unknown')
        
        # Convert to DataFrame
        features_df = pd.DataFrame(features_list)
        self.feature_names = features_df.columns.tolist()
        
        # Encode labels
        self.label_encoder.fit(labels_list)
        encoded_labels = self.label_encoder.transform(labels_list)
        
        return features_df.values, encoded_labels
    
    def train(self, users_df, roles_df=None, test_size=0.2):
        """Train the classifier"""
        print("Training classifier...")
        
        X, y = self.prepare_features(users_df, roles_df)
        
        # Split data with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Check if we have enough samples per class
        from collections import Counter
        train_counts = Counter(y_train)
        test_counts = Counter(y_test)
        print(f"Training samples per class: {dict(train_counts)}")
        print(f"Test samples per class: {dict(test_counts)}")
        
        # Train model
        print(f"Training {self.model_type} on {len(X_train)} samples...")
        self.model.fit(X_train, y_train)
        
        # Evaluate on test set
        y_pred = self.model.predict(X_test)
        
        # Also do cross-validation for more reliable accuracy estimate
        from sklearn.model_selection import cross_val_score
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5, scoring='accuracy')
        print(f"\nCross-validation accuracy (5-fold): {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Check for overfitting: compare train vs test accuracy
        y_train_pred = self.model.predict(X_train)
        train_accuracy = accuracy_score(y_train, y_train_pred)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"\nModel Performance:")
        print(f"Train Accuracy: {train_accuracy:.4f}")
        print(f"Test Accuracy: {accuracy:.4f}")
        print(f"Overfitting Gap: {train_accuracy - accuracy:.4f} (should be < 0.15)")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        # Warn if overfitting detected
        if train_accuracy - accuracy > 0.15:
            print("\n⚠️  WARNING: Potential overfitting detected! Train accuracy is significantly higher than test accuracy.")
            print("   Consider: reducing max_depth, increasing min_samples_split, or adding more regularization.")
        
        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"\nTop 10 Important Features:")
            for feature, importance in top_features:
                print(f"  {feature}: {importance:.4f}")
        
        self.is_trained = True
        
        return {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1)
        }
    
    def predict(self, user_features):
        """Predict career role for a user"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        # Prepare feature vector
        feature_vector = np.zeros(len(self.feature_names))
        
        for i, feature_name in enumerate(self.feature_names):
            if feature_name in user_features:
                feature_vector[i] = user_features[feature_name]
            elif feature_name.startswith('skill_'):
                skill = feature_name.replace('skill_', '')
                user_skills = user_features.get('skills', [])
                if isinstance(user_skills, list):
                    feature_vector[i] = 1 if any(skill.lower() in str(s).lower() for s in user_skills) else 0
        
        # Predict
        prediction = self.model.predict([feature_vector])[0]
        probabilities = self.model.predict_proba([feature_vector])[0]
        
        # Get top predictions
        top_indices = np.argsort(probabilities)[::-1][:5]
        
        results = []
        for idx in top_indices:
            results.append({
                'role': self.label_encoder.inverse_transform([idx])[0],
                'probability': float(probabilities[idx])
            })
        
        return results
    
    def get_feature_importance(self):
        """Get feature importance"""
        if not self.is_trained or not hasattr(self.model, 'feature_importances_'):
            return {}
        
        return dict(zip(self.feature_names, self.model.feature_importances_))
    
    def save(self, model_dir='ml/models'):
        """Save the model"""
        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Save model
        joblib.dump(self.model, model_path / 'career_classifier.joblib')
        joblib.dump(self.label_encoder, model_path / 'label_encoder.joblib')
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'n_estimators': self.n_estimators if self.model_type == 'random_forest' else None,
            'max_depth': self.max_depth,
            'feature_names': self.feature_names,
            'n_classes': len(self.label_encoder.classes_),
            'classes': self.label_encoder.classes_.tolist(),
            'is_trained': self.is_trained
        }
        
        with open(model_path / 'classifier_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to {model_path}")

def main():
    """Train classifier"""
    print("Training career role classifier...")
    
    data_dir = Path('data/processed')
    
    # Load user data
    users_df = pd.read_csv(data_dir / 'resumes_processed.csv') if (data_dir / 'resumes_processed.csv').exists() else None
    
    # Create sample data if not available
    if users_df is None or len(users_df) == 0:
        print("No user data found, creating sample data...")
        n_samples = 2000  # More samples for better accuracy
        
        roles = [
            'Data Scientist', 'Software Engineer', 'ML Engineer', 'Data Analyst',
            'Backend Developer', 'Frontend Developer', 'Full Stack Developer',
            'DevOps Engineer', 'Product Manager', 'UX Designer'
        ]
        
        # Create more distinct patterns for better classification
        data_rows = []
        for i in range(n_samples):
            role_idx = i % len(roles)
            role = roles[role_idx]
            
                # Create role-specific skill patterns with high distinctiveness
            if 'Data Scientist' in role:
                skills = ['python', 'sql', 'machine learning', 'pandas', 'numpy', 'statistics', 'data science']
                exp_years = np.random.randint(2, 8)
                education = ['master'] if np.random.random() > 0.3 else ['bachelor']
            elif 'ML Engineer' in role:
                skills = ['python', 'machine learning', 'tensorflow', 'pytorch', 'aws', 'docker']
                exp_years = np.random.randint(2, 7)
                education = ['master'] if np.random.random() > 0.4 else ['bachelor']
            elif 'Data Analyst' in role:
                skills = ['python', 'sql', 'pandas', 'analytics', 'statistics']
                exp_years = np.random.randint(1, 6)
                education = ['bachelor'] if np.random.random() > 0.4 else ['master']
            elif 'Software Engineer' in role or 'Backend Developer' in role:
                skills = ['java', 'spring', 'sql', 'rest api', 'microservices', 'git']
                exp_years = np.random.randint(1, 7)
                education = ['bachelor'] if np.random.random() > 0.4 else ['master']
            elif 'Frontend Developer' in role:
                skills = ['javascript', 'react', 'html', 'css', 'typescript', 'node.js']
                exp_years = np.random.randint(1, 6)
                education = ['bachelor'] if np.random.random() > 0.5 else ['master']
            elif 'Full Stack Developer' in role:
                skills = ['javascript', 'react', 'node.js', 'sql', 'rest api', 'html', 'css']
                exp_years = np.random.randint(2, 7)
                education = ['bachelor'] if np.random.random() > 0.5 else ['master']
            elif 'DevOps Engineer' in role:
                skills = ['docker', 'kubernetes', 'aws', 'linux', 'ci/cd', 'git']
                exp_years = np.random.randint(2, 8)
                education = ['bachelor'] if np.random.random() > 0.4 else ['master']
            elif 'Product Manager' in role:
                skills = ['agile', 'scrum', 'product management', 'analytics', 'jira', 'confluence']
                exp_years = np.random.randint(3, 10)
                education = ['master'] if np.random.random() > 0.5 else ['bachelor']
            elif 'UX Designer' in role:
                skills = ['design', 'figma', 'user research', 'prototyping', 'html', 'css']
                exp_years = np.random.randint(1, 6)
                education = ['bachelor'] if np.random.random() > 0.3 else ['master']
            else:
                skills = ['python', 'sql', 'git']
                exp_years = np.random.randint(0, 5)
                education = ['bachelor']
            
            # Add realistic noise to prevent overfitting (30% chance)
            # This simulates real-world data where roles have overlapping skills
            if np.random.random() < 0.3:
                # Add some cross-role skills to make data more realistic
                cross_skills = ['git', 'jira', 'agile', 'communication', 'problem solving', 
                              'teamwork', 'project management', 'documentation']
                skills.append(np.random.choice(cross_skills))
            
            # Add some variation in skill counts (not all roles have same number)
            if np.random.random() < 0.2:
                # Remove a random skill occasionally
                if len(skills) > 3:
                    skills.pop(np.random.randint(0, len(skills)))
            
            data_rows.append({
                'id': i,
                'skills_cleaned': skills,
                'experience_years': exp_years,
                'current_role': role,
                'target_role': role,  # Target matches current for training
                'education': education
            })
        
        users_df = pd.DataFrame(data_rows)
    
    # Train model with anti-overfitting hyperparameters
    # Reduced max_depth and increased min_samples_split to prevent overfitting
    classifier = CareerRoleClassifier(model_type='random_forest', n_estimators=200, max_depth=15, min_samples_split=10)
    metrics = classifier.train(users_df)
    
    # Save model
    classifier.save()
    
    print("Classifier training complete!")

if __name__ == '__main__':
    main()

