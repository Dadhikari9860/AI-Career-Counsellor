"""
Learning Roadmap Service
Generates structured week-by-week learning paths for skills and roles
"""

from typing import List, Dict, Optional
from app.services.ml_service import ml_service

class LearningRoadmapService:
    """Service to generate structured learning roadmaps"""
    
    def __init__(self):
        # Skill prerequisites and dependencies
        self.skill_prerequisites = {
            'react': ['javascript', 'html', 'css'],
            'angular': ['javascript', 'typescript', 'html', 'css'],
            'vue.js': ['javascript', 'html', 'css'],
            'node.js': ['javascript'],
            'django': ['python', 'sql'],
            'flask': ['python', 'sql'],
            'spring': ['java', 'sql'],
            'machine learning': ['python', 'statistics', 'linear algebra'],
            'deep learning': ['machine learning', 'python', 'neural networks'],
            'data science': ['python', 'sql', 'statistics'],
            'mongodb': ['javascript', 'node.js'],
            'postgresql': ['sql', 'database design'],
            'docker': ['linux', 'command line'],
            'kubernetes': ['docker', 'linux', 'networking'],
            'aws': ['linux', 'networking'],
            'full stack developer': ['html', 'css', 'javascript', 'sql', 'node.js', 'react'],
        }
        
        # Skill learning time estimates (in weeks)
        self.skill_learning_time = {
            'html': 1,
            'css': 1,
            'javascript': 3,
            'python': 3,
            'java': 4,
            'sql': 2,
            'react': 3,
            'node.js': 2,
            'django': 2,
            'flask': 2,
            'machine learning': 6,
            'data science': 6,
            'docker': 2,
            'aws': 4,
            'database': 3,
            'mongodb': 2,
            'postgresql': 2,
        }
        
        # Learning topics for each skill (week-by-week breakdown)
        self.skill_topics = {
            'database': [
                {'week': 1, 'topics': ['Introduction to databases', 'Relational vs NoSQL', 'SQL basics', 'SELECT queries'], 'hours': 10},
                {'week': 2, 'topics': ['JOIN operations', 'Aggregate functions', 'Subqueries', 'Data types'], 'hours': 12},
                {'week': 3, 'topics': ['Database design', 'Normalization', 'Indexes', 'Transactions'], 'hours': 10},
            ],
            'sql': [
                {'week': 1, 'topics': ['SQL basics', 'SELECT statements', 'WHERE clauses', 'Sorting and filtering'], 'hours': 10},
                {'week': 2, 'topics': ['JOINs (INNER, LEFT, RIGHT)', 'Aggregate functions', 'GROUP BY', 'HAVING'], 'hours': 12},
            ],
            'python': [
                {'week': 1, 'topics': ['Python basics', 'Variables and data types', 'Control flow', 'Functions'], 'hours': 12},
                {'week': 2, 'topics': ['Data structures (lists, dicts)', 'File handling', 'Error handling', 'Modules'], 'hours': 12},
                {'week': 3, 'topics': ['Object-oriented programming', 'Libraries (pandas, numpy)', 'APIs', 'Projects'], 'hours': 15},
            ],
            'javascript': [
                {'week': 1, 'topics': ['JavaScript basics', 'Variables and data types', 'Functions', 'DOM manipulation'], 'hours': 12},
                {'week': 2, 'topics': ['Arrays and objects', 'ES6 features', 'Async/await', 'Promises'], 'hours': 12},
                {'week': 3, 'topics': ['Event handling', 'APIs and fetch', 'Local storage', 'Projects'], 'hours': 15},
            ],
            'react': [
                {'week': 1, 'topics': ['React basics', 'Components', 'JSX', 'Props'], 'hours': 12},
                {'week': 2, 'topics': ['State management', 'Hooks (useState, useEffect)', 'Event handling', 'Forms'], 'hours': 15},
                {'week': 3, 'topics': ['React Router', 'Context API', 'Custom hooks', 'Build a project'], 'hours': 15},
            ],
            'machine learning': [
                {'week': 1, 'topics': ['Python basics review', 'NumPy and Pandas', 'Data visualization', 'Statistics basics'], 'hours': 15},
                {'week': 2, 'topics': ['Linear regression', 'Logistic regression', 'Model evaluation', 'Scikit-learn'], 'hours': 15},
                {'week': 3, 'topics': ['Classification algorithms', 'Decision trees', 'Random forests', 'Cross-validation'], 'hours': 15},
                {'week': 4, 'topics': ['Clustering', 'Dimensionality reduction', 'Feature engineering', 'Projects'], 'hours': 15},
                {'week': 5, 'topics': ['Neural networks basics', 'TensorFlow/Keras', 'Deep learning concepts'], 'hours': 15},
                {'week': 6, 'topics': ['Advanced models', 'Model deployment', 'MLOps basics', 'Capstone project'], 'hours': 15},
            ],
            'data science': [
                {'week': 1, 'topics': ['Python for data science', 'Pandas basics', 'Data cleaning', 'Exploratory data analysis'], 'hours': 15},
                {'week': 2, 'topics': ['Data visualization (Matplotlib, Seaborn)', 'Statistical analysis', 'Hypothesis testing'], 'hours': 15},
                {'week': 3, 'topics': ['Machine learning basics', 'Regression models', 'Classification models'], 'hours': 15},
                {'week': 4, 'topics': ['Feature engineering', 'Model evaluation', 'Cross-validation'], 'hours': 15},
                {'week': 5, 'topics': ['Time series analysis', 'Advanced visualization', 'Data storytelling'], 'hours': 15},
                {'week': 6, 'topics': ['Big data tools', 'Data pipelines', 'Capstone project'], 'hours': 15},
            ],
            'node.js': [
                {'week': 1, 'topics': ['Node.js basics', 'NPM and packages', 'File system operations', 'Modules'], 'hours': 12},
                {'week': 2, 'topics': ['Express.js framework', 'Routing', 'Middleware', 'REST APIs'], 'hours': 15},
            ],
            'docker': [
                {'week': 1, 'topics': ['Docker basics', 'Containers vs VMs', 'Docker images', 'Dockerfile'], 'hours': 10},
                {'week': 2, 'topics': ['Docker Compose', 'Networking', 'Volumes', 'Best practices'], 'hours': 10},
            ],
        }
    
    def generate_roadmap_for_skill(self, skill: str, user_skills: List[str] = None) -> Dict:
        """Generate a week-by-week learning roadmap for a specific skill"""
        skill_lower = skill.lower().strip()
        user_skills_lower = [s.lower() if isinstance(s, str) else str(s).lower() for s in (user_skills or [])]
        
        # Check if we have predefined topics for this skill
        if skill_lower in self.skill_topics:
            roadmap = {
                'skill': skill,
                'weeks': self.skill_topics[skill_lower],
                'total_weeks': len(self.skill_topics[skill_lower]),
                'estimated_total_hours': sum(w['hours'] for w in self.skill_topics[skill_lower]),
                'prerequisites': self._get_prerequisites(skill_lower, user_skills_lower),
                'learning_resources': self._get_resource_recommendations(skill_lower)
            }
        else:
            # Generate generic roadmap
            learning_time = self.skill_learning_time.get(skill_lower, 3)
            roadmap = {
                'skill': skill,
                'weeks': self._generate_generic_weeks(skill, learning_time),
                'total_weeks': learning_time,
                'estimated_total_hours': learning_time * 12,
                'prerequisites': self._get_prerequisites(skill_lower, user_skills_lower),
                'learning_resources': self._get_resource_recommendations(skill_lower)
            }
        
        return roadmap
    
    def generate_roadmap_for_role(self, target_role: str, user_skills: List[str] = None) -> Dict:
        """Generate a comprehensive learning roadmap for a target role"""
        from app.utils.role_helpers import find_role_by_name
        
        role = find_role_by_name(target_role)
        if not role:
            return None
        
        # Get skill gap
        skill_gap = ml_service.analyze_skill_gap(
            user_skills or [],
            role.required_skills or []
        )
        
        missing_skills = skill_gap.get('missing_skills', [])
        
        # Order skills by prerequisites
        ordered_skills = self._order_skills_by_prerequisites(missing_skills, user_skills or [])
        
        # Generate week-by-week plan
        weeks = []
        current_week = 1
        
        for skill in ordered_skills[:10]:  # Limit to top 10 skills
            skill_roadmap = self.generate_roadmap_for_skill(skill, user_skills)
            
            for week_plan in skill_roadmap['weeks']:
                weeks.append({
                    'week': current_week,
                    'skill': skill,
                    'topics': week_plan['topics'],
                    'hours': week_plan['hours'],
                    'focus': f"Learning {skill.title()}"
                })
                current_week += 1
        
        return {
            'target_role': target_role,
            'total_weeks': len(weeks),
            'estimated_total_hours': sum(w['hours'] for w in weeks),
            'weeks': weeks[:12],  # Limit to 12 weeks for display
            'missing_skills': missing_skills,
            'matching_skills': skill_gap.get('matching_skills', []),
            'match_percentage': skill_gap.get('match_percentage', 0)
        }
    
    def _get_prerequisites(self, skill: str, user_skills: List[str]) -> Dict:
        """Get prerequisites for a skill and check if user has them"""
        prerequisites = self.skill_prerequisites.get(skill, [])
        
        missing_prereqs = []
        has_prereqs = []
        
        for prereq in prerequisites:
            if any(prereq.lower() in us or us in prereq.lower() for us in user_skills):
                has_prereqs.append(prereq)
            else:
                missing_prereqs.append(prereq)
        
        return {
            'required': prerequisites,
            'has': has_prereqs,
            'missing': missing_prereqs,
            'ready': len(missing_prereqs) == 0
        }
    
    def _order_skills_by_prerequisites(self, skills: List[str], user_skills: List[str]) -> List[str]:
        """Order skills so prerequisites come first"""
        ordered = []
        remaining = skills.copy()
        user_skills_lower = [s.lower() if isinstance(s, str) else str(s).lower() for s in user_skills]
        
        while remaining:
            # Find skills with no missing prerequisites
            for skill in remaining:
                prereqs = self.skill_prerequisites.get(skill.lower(), [])
                missing_prereqs = [p for p in prereqs if not any(p.lower() in us or us in p.lower() for us in user_skills_lower)]
                
                # If no missing prerequisites or prerequisites already in ordered list
                if not missing_prereqs or all(p in ordered for p in prereqs):
                    ordered.append(skill)
                    remaining.remove(skill)
                    user_skills_lower.append(skill.lower())
                    break
            else:
                # If we can't find any skill without prerequisites, just add the first one
                if remaining:
                    ordered.append(remaining[0])
                    user_skills_lower.append(remaining[0].lower())
                    remaining.pop(0)
        
        return ordered
    
    def _generate_generic_weeks(self, skill: str, num_weeks: int) -> List[Dict]:
        """Generate generic week-by-week plan for a skill"""
        weeks = []
        for i in range(num_weeks):
            if i == 0:
                topics = [f'{skill.title()} basics', 'Introduction and setup', 'Core concepts', 'First steps']
            elif i == num_weeks - 1:
                topics = ['Advanced concepts', 'Best practices', 'Real-world projects', 'Review and practice']
            else:
                topics = [f'Intermediate {skill.title()}', 'Advanced features', 'Practical exercises', 'Building projects']
            
            weeks.append({
                'week': i + 1,
                'topics': topics,
                'hours': 12
            })
        
        return weeks
    
    def _get_resource_recommendations(self, skill: str) -> List[str]:
        """Get recommended resource types for a skill"""
        return [
            f"Watch {skill.title()} tutorial videos",
            f"Practice with {skill.title()} exercises",
            f"Build a {skill.title()} project",
            f"Read {skill.title()} documentation",
            f"Join {skill.title()} community forums"
        ]

