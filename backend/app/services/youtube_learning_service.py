"""
YouTube Learning Resource Service
Maps skills to YouTube learning resources based on skill gap analysis
"""

import json
import urllib.parse
from typing import List, Dict, Optional
from pathlib import Path

class YouTubeLearningService:
    """Service to recommend YouTube videos based on skill gaps"""
    
    def __init__(self):
        self.skill_to_youtube_map = self._load_skill_mappings()
        self.popular_channels = self._get_popular_channels()
    
    def _load_skill_mappings(self) -> Dict[str, Dict]:
        """Load skill to YouTube video/channel mappings"""
        # Comprehensive mapping of skills to YouTube resources
        # This can be extended with a dataset or API
        return {
            'python': {
                'channels': ['freeCodeCamp.org', 'Corey Schafer', 'Programming with Mosh', 'Traversy Media'],
                'search_terms': ['python tutorial', 'python programming', 'learn python'],
                'playlists': ['Python Full Course', 'Python for Beginners', 'Python Projects'],
                'difficulty': 'beginner'
            },
            'javascript': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja', 'Programming with Mosh'],
                'search_terms': ['javascript tutorial', 'learn javascript', 'js tutorial'],
                'playlists': ['JavaScript Full Course', 'JavaScript for Beginners', 'Modern JavaScript'],
                'difficulty': 'beginner'
            },
            'react': {
                'channels': ['Traversy Media', 'freeCodeCamp.org', 'The Net Ninja', 'Programming with Mosh'],
                'search_terms': ['react tutorial', 'react course', 'learn react'],
                'playlists': ['React Full Course', 'React for Beginners', 'React Hooks'],
                'difficulty': 'intermediate'
            },
            'node.js': {
                'channels': ['Traversy Media', 'freeCodeCamp.org', 'The Net Ninja'],
                'search_terms': ['nodejs tutorial', 'node.js course', 'learn nodejs'],
                'playlists': ['Node.js Full Course', 'Node.js Tutorial', 'Express.js'],
                'difficulty': 'intermediate'
            },
            'java': {
                'channels': ['freeCodeCamp.org', 'Programming with Mosh', 'Derek Banas'],
                'search_terms': ['java tutorial', 'learn java', 'java programming'],
                'playlists': ['Java Full Course', 'Java for Beginners', 'Java OOP'],
                'difficulty': 'beginner'
            },
            'sql': {
                'channels': ['freeCodeCamp.org', 'Programming with Mosh', 'Traversy Media'],
                'search_terms': ['sql tutorial', 'learn sql', 'database tutorial'],
                'playlists': ['SQL Full Course', 'SQL for Beginners', 'MySQL Tutorial'],
                'difficulty': 'beginner'
            },
            'database': {
                'channels': ['freeCodeCamp.org', 'Programming with Mosh', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['database tutorial', 'learn database', 'sql database', 'database design'],
                'playlists': ['Database Full Course', 'SQL Database Tutorial', 'Database Design', 'MySQL Tutorial', 'PostgreSQL Tutorial'],
                'difficulty': 'beginner'
            },
            'machine learning': {
                'channels': ['3Blue1Brown', 'StatQuest', 'freeCodeCamp.org', 'Sentdex'],
                'search_terms': ['machine learning tutorial', 'ml course', 'learn ml'],
                'playlists': ['Machine Learning Course', 'ML for Beginners', 'Deep Learning'],
                'difficulty': 'advanced'
            },
            'data science': {
                'channels': ['freeCodeCamp.org', 'StatQuest', 'Corey Schafer', 'Krish Naik'],
                'search_terms': ['data science tutorial', 'data science course', 'learn data science'],
                'playlists': ['Data Science Full Course', 'Python for Data Science', 'Pandas Tutorial'],
                'difficulty': 'intermediate'
            },
            'aws': {
                'channels': ['freeCodeCamp.org', 'AWS', 'Simplilearn', 'Edureka'],
                'search_terms': ['aws tutorial', 'aws course', 'learn aws'],
                'playlists': ['AWS Full Course', 'AWS for Beginners', 'AWS Certification'],
                'difficulty': 'intermediate'
            },
            'docker': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'Docker', 'TechWorld with Nana'],
                'search_terms': ['docker tutorial', 'docker course', 'learn docker'],
                'playlists': ['Docker Full Course', 'Docker for Beginners', 'Docker Compose'],
                'difficulty': 'intermediate'
            },
            'kubernetes': {
                'channels': ['freeCodeCamp.org', 'TechWorld with Nana', 'Kubernetes'],
                'search_terms': ['kubernetes tutorial', 'k8s course', 'learn kubernetes'],
                'playlists': ['Kubernetes Full Course', 'K8s Tutorial', 'Kubernetes for Beginners'],
                'difficulty': 'advanced'
            },
            'git': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'Corey Schafer'],
                'search_terms': ['git tutorial', 'github tutorial', 'learn git'],
                'playlists': ['Git Full Course', 'Git for Beginners', 'GitHub Tutorial'],
                'difficulty': 'beginner'
            },
            'html': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['html tutorial', 'html5 course', 'learn html'],
                'playlists': ['HTML Full Course', 'HTML for Beginners', 'HTML5 Tutorial'],
                'difficulty': 'beginner'
            },
            'css': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja', 'Web Dev Simplified'],
                'search_terms': ['css tutorial', 'css3 course', 'learn css'],
                'playlists': ['CSS Full Course', 'CSS for Beginners', 'CSS Grid & Flexbox'],
                'difficulty': 'beginner'
            },
            'typescript': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['typescript tutorial', 'ts course', 'learn typescript'],
                'playlists': ['TypeScript Full Course', 'TypeScript Tutorial', 'TS for Beginners'],
                'difficulty': 'intermediate'
            },
            'angular': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['angular tutorial', 'angular course', 'learn angular'],
                'playlists': ['Angular Full Course', 'Angular Tutorial', 'Angular for Beginners'],
                'difficulty': 'intermediate'
            },
            'vue.js': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['vue tutorial', 'vuejs course', 'learn vue'],
                'playlists': ['Vue.js Full Course', 'Vue Tutorial', 'Vue for Beginners'],
                'difficulty': 'intermediate'
            },
            'django': {
                'channels': ['freeCodeCamp.org', 'Corey Schafer', 'Traversy Media'],
                'search_terms': ['django tutorial', 'django course', 'learn django'],
                'playlists': ['Django Full Course', 'Django Tutorial', 'Django for Beginners'],
                'difficulty': 'intermediate'
            },
            'flask': {
                'channels': ['freeCodeCamp.org', 'Corey Schafer', 'Traversy Media'],
                'search_terms': ['flask tutorial', 'flask course', 'learn flask'],
                'playlists': ['Flask Full Course', 'Flask Tutorial', 'Flask for Beginners'],
                'difficulty': 'intermediate'
            },
            'mongodb': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['mongodb tutorial', 'mongo course', 'learn mongodb'],
                'playlists': ['MongoDB Full Course', 'MongoDB Tutorial', 'NoSQL Database'],
                'difficulty': 'intermediate'
            },
            'postgresql': {
                'channels': ['freeCodeCamp.org', 'Programming with Mosh', 'Traversy Media'],
                'search_terms': ['postgresql tutorial', 'postgres course', 'learn postgresql'],
                'playlists': ['PostgreSQL Full Course', 'PostgreSQL Tutorial', 'SQL Database'],
                'difficulty': 'intermediate'
            },
            'rest api': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['rest api tutorial', 'api course', 'learn rest api'],
                'playlists': ['REST API Full Course', 'API Tutorial', 'RESTful API'],
                'difficulty': 'intermediate'
            },
            'graphql': {
                'channels': ['freeCodeCamp.org', 'Traversy Media', 'The Net Ninja'],
                'search_terms': ['graphql tutorial', 'graphql course', 'learn graphql'],
                'playlists': ['GraphQL Full Course', 'GraphQL Tutorial', 'GraphQL API'],
                'difficulty': 'intermediate'
            },
            'microservices': {
                'channels': ['freeCodeCamp.org', 'TechWorld with Nana', 'Java Brains'],
                'search_terms': ['microservices tutorial', 'microservices course', 'learn microservices'],
                'playlists': ['Microservices Full Course', 'Microservices Architecture', 'System Design'],
                'difficulty': 'advanced'
            },
            'ci/cd': {
                'channels': ['freeCodeCamp.org', 'TechWorld with Nana', 'Traversy Media'],
                'search_terms': ['ci cd tutorial', 'devops course', 'learn ci cd'],
                'playlists': ['CI/CD Full Course', 'Jenkins Tutorial', 'DevOps Pipeline'],
                'difficulty': 'intermediate'
            },
            'terraform': {
                'channels': ['freeCodeCamp.org', 'TechWorld with Nana', 'HashiCorp'],
                'search_terms': ['terraform tutorial', 'terraform course', 'learn terraform'],
                'playlists': ['Terraform Full Course', 'Terraform Tutorial', 'IaC Tutorial'],
                'difficulty': 'intermediate'
            },
            'linux': {
                'channels': ['freeCodeCamp.org', 'LearnLinuxTV', 'NetworkChuck'],
                'search_terms': ['linux tutorial', 'linux course', 'learn linux'],
                'playlists': ['Linux Full Course', 'Linux for Beginners', 'Linux Commands'],
                'difficulty': 'beginner'
            },
            'cybersecurity': {
                'channels': ['NetworkChuck', 'freeCodeCamp.org', 'Professor Messer'],
                'search_terms': ['cybersecurity tutorial', 'security course', 'learn cybersecurity'],
                'playlists': ['Cybersecurity Full Course', 'Ethical Hacking', 'Network Security'],
                'difficulty': 'intermediate'
            },
            'data structures': {
                'channels': ['freeCodeCamp.org', 'Abdul Bari', 'Back To Back SWE'],
                'search_terms': ['data structures tutorial', 'dsa course', 'learn data structures'],
                'playlists': ['Data Structures Full Course', 'DSA Tutorial', 'Algorithms'],
                'difficulty': 'intermediate'
            },
            'algorithms': {
                'channels': ['freeCodeCamp.org', 'Abdul Bari', 'Back To Back SWE'],
                'search_terms': ['algorithms tutorial', 'algo course', 'learn algorithms'],
                'playlists': ['Algorithms Full Course', 'Algorithm Tutorial', 'DSA Course'],
                'difficulty': 'intermediate'
            }
        }
    
    def _get_popular_channels(self) -> List[str]:
        """Get list of popular tech education channels"""
        return [
            'freeCodeCamp.org',
            'Traversy Media',
            'Programming with Mosh',
            'The Net Ninja',
            'Corey Schafer',
            'TechWorld with Nana',
            'NetworkChuck',
            '3Blue1Brown',
            'StatQuest',
            'Web Dev Simplified'
        ]
    
    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill name for matching"""
        skill_lower = skill.lower().strip()
        
        # Handle variations
        skill_variations = {
            'js': 'javascript',
            'nodejs': 'node.js',
            'node': 'node.js',
            'reactjs': 'react',
            'vuejs': 'vue.js',
            'angularjs': 'angular',
            'ml': 'machine learning',
            'ds': 'data science',
            'dsa': 'data structures',
            'algo': 'algorithms',
            'db': 'database',
            'databases': 'database',
            'sql database': 'database',
            'rest': 'rest api',
            'api': 'rest api',
            'k8s': 'kubernetes',
            'cicd': 'ci/cd',
            'devops': 'ci/cd',
            'full stack': 'full stack developer',
            'fullstack': 'full stack developer'
        }
        
        return skill_variations.get(skill_lower, skill_lower)
    
    def get_youtube_resources_for_skill(self, skill: str, limit: int = 3) -> List[Dict]:
        """Get YouTube learning resources for a specific skill"""
        normalized_skill = self._normalize_skill(skill)
        
        # Check if we have a direct mapping
        skill_data = self.skill_to_youtube_map.get(normalized_skill)
        
        resources = []
        
        if skill_data:
            # Create resources based on channels and playlists
            channels = skill_data.get('channels', [])
            playlists = skill_data.get('playlists', [])
            search_terms = skill_data.get('search_terms', [normalized_skill + ' tutorial'])
            difficulty = skill_data.get('difficulty', 'intermediate')
            
            # Create YouTube search URLs
            for i, search_term in enumerate(search_terms[:limit]):
                search_encoded = urllib.parse.quote(search_term)
                youtube_url = f"https://www.youtube.com/results?search_query={search_encoded}"
                
                # Try to get a specific channel if available
                channel = channels[i % len(channels)] if channels else None
                playlist = playlists[i % len(playlists)] if playlists else None
                
                resource = {
                    'id': f"youtube_{normalized_skill}_{i}",
                    'title': f"{skill.title()} Tutorial - {playlist or search_term.title()}",
                    'description': f"Learn {skill} with this comprehensive tutorial. "
                                 f"{f'From {channel}' if channel else ''} "
                                 f"{f'Playlist: {playlist}' if playlist else ''}",
                    'resource_type': 'video',
                    'url': youtube_url,
                    'provider': 'YouTube',
                    'channel': channel,
                    'playlist': playlist,
                    'skills_covered': [skill],
                    'difficulty_level': difficulty,
                    'duration': 'Varies',
                    'source': 'youtube'
                }
                resources.append(resource)
        else:
            # Fallback: create generic YouTube search
            search_encoded = urllib.parse.quote(f"{skill} tutorial")
            youtube_url = f"https://www.youtube.com/results?search_query={search_encoded}"
            
            resource = {
                'id': f"youtube_{normalized_skill}_0",
                'title': f"Learn {skill.title()} - YouTube Tutorials",
                'description': f"Find the best YouTube tutorials to learn {skill}. "
                             f"Search through thousands of free video tutorials from top educators.",
                'resource_type': 'video',
                'url': youtube_url,
                'provider': 'YouTube',
                'skills_covered': [skill],
                'difficulty_level': 'beginner',
                'duration': 'Varies',
                'source': 'youtube'
            }
            resources.append(resource)
        
        return resources
    
    def get_learning_resources_for_skill_gap(self, missing_skills: List[str], limit_per_skill: int = 2) -> List[Dict]:
        """Get YouTube learning resources for multiple missing skills"""
        all_resources = []
        seen_titles = set()
        
        for skill in missing_skills:
            resources = self.get_youtube_resources_for_skill(skill, limit=limit_per_skill)
            
            for resource in resources:
                # Avoid duplicates
                title_key = resource['title'].lower()
                if title_key not in seen_titles:
                    seen_titles.add(title_key)
                    resource['missing_skill'] = skill  # Tag which skill it addresses
                    all_resources.append(resource)
        
        return all_resources
    
    def get_channel_url(self, channel_name: str) -> str:
        """Get YouTube channel URL from channel name"""
        channel_encoded = urllib.parse.quote(channel_name)
        return f"https://www.youtube.com/results?search_query={channel_encoded}&sp=EgIQAg%253D%253D"
    
    def get_playlist_url(self, playlist_name: str, channel_name: str = None) -> str:
        """Get YouTube playlist search URL"""
        if channel_name:
            search_query = f"{channel_name} {playlist_name}"
        else:
            search_query = playlist_name
        search_encoded = urllib.parse.quote(search_query)
        return f"https://www.youtube.com/results?search_query={search_encoded}&sp=EgIQAw%253D%253D"

