"""
Chatbot routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, CareerRole, Job, LearningResource
from app.services.ml_service import ml_service
from app.services.job_scraper import JobScraper
from app.utils.auth_helpers import get_current_user_id
from app.utils.role_helpers import find_role_by_name

bp = Blueprint('chatbot', __name__)

@bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    """Chatbot endpoint"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Classify intent
    intent_result = ml_service.classify_intent(message)
    intent = intent_result['intent']
    confidence = intent_result['confidence']
    
    # Generate response based on intent
    response = {
        'message': '',
        'intent': intent,
        'confidence': confidence,
        'data': {},
        'suggestions': []  # Interactive suggestions
    }
    
    if intent == 'career_advice':
        # Get career recommendations
        user_features = {
            'skills': user.skills or [],
            'experience_years': user.experience_years or 0,
            'current_role': user.current_role or '',
            'interests': user.interests or []
        }
        recommendations = ml_service.get_hybrid_recommendations(user_features, top_k=5)
        
        roles = []
        for rec in recommendations['roles'][:3]:
            role_name = rec.get('role')
            if role_name:
                role = find_role_by_name(role_name)
                if role:
                    roles.append(role.to_dict())
        
        if roles:
            role_names = ', '.join([r['title'] for r in roles])
            response['message'] = f"Based on your profile, I recommend these career paths: {role_names}. Would you like to:\n• See detailed information about any role?\n• Check skill gaps for a specific role?\n• Get a learning path?"
            response['data'] = {'recommended_roles': roles}
            response['suggestions'] = [
                f"Tell me more about {roles[0]['title']}",
                f"Show skill gap for {roles[0]['title']}",
                "Get learning path",
                "Compare these roles"
            ]
        else:
            response['message'] = "I'd be happy to help you with career advice! Could you tell me more about your skills and interests?"
            response['suggestions'] = ["Update my profile", "Show available careers", "What skills do I need?"]
    
    elif intent == 'job_search':
        # Get job recommendations with real-time scraping
        user_skills = [s if isinstance(s, str) else s.get('name', '') for s in (user.skills or [])]
        target_role = user.target_role or user.current_role or 'Software Engineer'
        
        scraper = JobScraper()
        user_location = user.location or ""  # Get user's location
        scraped_jobs = scraper.get_jobs_for_user(user_skills, target_role, user_location)
        
        # Also get jobs from database
        db_jobs = Job.query.limit(3).all()
        all_jobs = scraped_jobs + [job.to_dict() for job in db_jobs]
        
        if all_jobs:
            response['message'] = f"I found {len(all_jobs)} job opportunities matching your profile. Here are the top matches:"
            response['data'] = {'jobs': all_jobs[:5]}
            response['suggestions'] = [
                "Show more jobs",
                "Filter by location",
                "Show remote jobs only",
                "Update my job preferences"
            ]
        else:
            response['message'] = "I'm searching for jobs that match your profile. Would you like me to search for a specific role or location?"
            response['suggestions'] = ["Search for Full Stack Developer jobs", "Show remote jobs", "Update my profile"]
    
    elif intent == 'skill_gap':
        if user.target_role:
            target_role = find_role_by_name(user.target_role)
            if target_role:
                skill_gap = ml_service.analyze_skill_gap(
                    user.skills or [],
                    target_role.required_skills or []
                )
                match_pct = skill_gap['match_percentage']
                missing_count = len(skill_gap['missing_skills'])
                
                if match_pct >= 70:
                    response['message'] = f"Great news! For {user.target_role}, you have a {match_pct}% skill match. You're well-prepared! You only need to learn {missing_count} more skills."
                elif match_pct >= 40:
                    response['message'] = f"For {user.target_role}, you have a {match_pct}% skill match. You have {len(skill_gap['matching_skills'])} matching skills and need to learn {missing_count} more skills to be fully prepared."
                else:
                    response['message'] = f"For {user.target_role}, you have a {match_pct}% skill match. You need to learn {missing_count} key skills. Let me help you create a learning plan!"
                
                response['data'] = {
                    'skill_gap': skill_gap,
                    'target_role': target_role.to_dict()
                }
                response['suggestions'] = [
                    "Show learning resources",
                    "Create learning path",
                    "Compare with other roles",
                    "Update my skills"
                ]
        else:
            response['message'] = "To analyze your skill gap, please set a target role in your profile. Would you like me to help you choose one?"
            response['suggestions'] = ["Show available roles", "Update my profile", "Get career recommendations"]
    
    elif intent == 'learning_path':
        # Extract specific skill/topic from user message
        extracted_skill = _extract_skill_from_message(message)
        
        if extracted_skill:
            # Check if user is asking for learning path (roadmap) or just resources
            is_learning_path_request = any(phrase in message.lower() for phrase in [
                'learning path', 'study plan', 'roadmap', 'week by week', 'study schedule',
                'how to learn', 'what to study', 'learning plan'
            ])
            
            if is_learning_path_request:
                # Generate structured week-by-week learning roadmap for the skill
                try:
                    from app.services.learning_roadmap_service import LearningRoadmapService
                    roadmap_service = LearningRoadmapService()
                    roadmap = roadmap_service.generate_roadmap_for_skill(
                        extracted_skill,
                        user.skills or []
                    )
                    
                    response['message'] = f"Here's your {roadmap['total_weeks']}-week learning roadmap for '{extracted_skill}':\n\n"
                    response['message'] += f"**Total Time:** {roadmap['estimated_total_hours']} hours over {roadmap['total_weeks']} weeks\n\n"
                    
                    # Check prerequisites
                    if roadmap['prerequisites']['missing']:
                        response['message'] += f"**Prerequisites:** You may want to learn these first: {', '.join(roadmap['prerequisites']['missing'])}\n\n"
                    
                    response['message'] += "**Week-by-Week Plan:**\n"
                    
                    for week_plan in roadmap['weeks']:
                        response['message'] += f"\n**Week {week_plan['week']}** ({week_plan['hours']} hours)\n"
                        for topic in week_plan['topics']:
                            response['message'] += f"  • {topic}\n"
                    
                    response['data'] = {'learning_roadmap': roadmap}
                    response['suggestions'] = [
                        f"Show {extracted_skill} resources",
                        "Get learning path for my target role",
                        "Find related skills",
                        "Get skill verification quiz"
                    ]
                except Exception as e:
                    print(f"Error generating roadmap: {e}")
                    # Fallback to resources
                    is_learning_path_request = False
            
            if not is_learning_path_request:
                # User asked for specific skill - provide resources for that skill
                resources = []
                
                # Get YouTube resources for the specific skill
                try:
                    from app.services.youtube_learning_service import YouTubeLearningService
                    youtube_service = YouTubeLearningService()
                    youtube_resources = youtube_service.get_learning_resources_for_skill_gap(
                        [extracted_skill], 
                        limit_per_skill=5
                    )
                    resources.extend(youtube_resources)
                except Exception as e:
                    print(f"Error getting YouTube resources: {e}")
                
                # Also get resources from database for this specific skill
                resource_list = LearningResource.query.filter(
                    LearningResource.skills_covered.contains([extracted_skill])
                ).limit(5).all()
                
                for r in resource_list:
                    resource_dict = r.to_dict()
                    # Ensure YouTube URL if not present
                    if not resource_dict.get('url') or 'youtube' not in resource_dict.get('url', '').lower():
                        import urllib.parse
                        skill_encoded = urllib.parse.quote(f"{extracted_skill} tutorial")
                        resource_dict['url'] = f"https://www.youtube.com/results?search_query={skill_encoded}"
                        resource_dict['provider'] = 'YouTube'
                        resource_dict['resource_type'] = 'video'
                    resource_dict['missing_skill'] = extracted_skill
                    # Avoid duplicates
                    if not any(res.get('id') == resource_dict.get('id') for res in resources):
                        resources.append(resource_dict)
                
                # If no resources found in DB, create YouTube search URLs
                if not resources:
                    import urllib.parse
                    skill_encoded = urllib.parse.quote(f"{extracted_skill} tutorial")
                    resources.append({
                        'id': f"youtube_{extracted_skill}",
                        'title': f"Learn {extracted_skill.title()} - YouTube Tutorials",
                        'description': f"Find the best YouTube tutorials to learn {extracted_skill}",
                        'url': f"https://www.youtube.com/results?search_query={skill_encoded}",
                        'resource_type': 'video',
                        'provider': 'YouTube',
                        'skills_covered': [extracted_skill],
                        'missing_skill': extracted_skill,
                        'source': 'youtube'
                    })
                
                if resources:
                    response['message'] = f"I found {len(resources)} learning resources for '{extracted_skill}'. Here are the best tutorials and courses to help you learn this skill:"
                    response['data'] = {'learning_resources': resources[:10]}
                    response['suggestions'] = [
                        f"Get {extracted_skill} learning roadmap",
                        f"Show more {extracted_skill} resources",
                        "Get learning path for my target role",
                        "Find related skills"
                    ]
                else:
                    response['message'] = f"I'm searching for learning resources for '{extracted_skill}'. Let me find the best tutorials and courses for you."
                    response['suggestions'] = [f"Get {extracted_skill} learning roadmap", "Search for another skill", "Get career advice"]
        
        elif user.target_role:
            # No specific skill mentioned - use target role skill gap
            # Check if user is asking for learning path (roadmap) or just resources
            is_learning_path_request = any(phrase in message.lower() for phrase in [
                'learning path', 'study plan', 'roadmap', 'week by week', 'study schedule',
                'how to learn', 'what to study', 'learning plan'
            ])
            
            if is_learning_path_request:
                # Generate structured week-by-week learning roadmap
                try:
                    from app.services.learning_roadmap_service import LearningRoadmapService
                    roadmap_service = LearningRoadmapService()
                    roadmap = roadmap_service.generate_roadmap_for_role(
                        user.target_role,
                        user.skills or []
                    )
                    
                    if roadmap:
                        response['message'] = f"Here's your personalized {roadmap['total_weeks']}-week learning roadmap to become a {user.target_role}:\n\n"
                        response['message'] += f"**Current Status:** {roadmap['match_percentage']:.1f}% skill match\n"
                        response['message'] += f"**Total Time:** {roadmap['estimated_total_hours']} hours over {roadmap['total_weeks']} weeks\n\n"
                        response['message'] += "**Week-by-Week Plan:**\n"
                        
                        for week_plan in roadmap['weeks']:
                            response['message'] += f"\n**Week {week_plan['week']}: {week_plan['focus']}** ({week_plan['hours']} hours)\n"
                            for topic in week_plan['topics']:
                                response['message'] += f"  • {topic}\n"
                        
                        response['data'] = {'learning_roadmap': roadmap}
                        response['suggestions'] = [
                            "Show detailed resources",
                            "Create study schedule",
                            "Track my progress",
                            "Get skill verification quiz"
                        ]
                    else:
                        response['message'] = f"I'm creating a personalized learning roadmap for {user.target_role}. Let me analyze your skill gap first."
                        response['suggestions'] = ["Show skill gap", "Get resources", "Update my profile"]
                except Exception as e:
                    print(f"Error generating roadmap: {e}")
                    response['message'] = f"To become a {user.target_role}, I'll help you create a learning plan. Let me analyze your skills first."
                    response['suggestions'] = ["Show skill gap", "Get resources", "Update my profile"]
            else:
                # Just show resources (backward compatibility)
                target_role = find_role_by_name(user.target_role)
                if target_role:
                    skill_gap = ml_service.analyze_skill_gap(
                        user.skills or [],
                        target_role.required_skills or []
                    )
                    resources = []
                    
                    # Get YouTube resources first
                    try:
                        from app.services.youtube_learning_service import YouTubeLearningService
                        youtube_service = YouTubeLearningService()
                        youtube_resources = youtube_service.get_learning_resources_for_skill_gap(
                            skill_gap['missing_skills'][:10], 
                            limit_per_skill=2
                        )
                        resources.extend(youtube_resources)
                    except Exception as e:
                        print(f"Error getting YouTube resources: {e}")
                    
                    # Also get resources from database
                    for skill in skill_gap['missing_skills'][:5]:
                        resource_list = LearningResource.query.filter(
                            LearningResource.skills_covered.contains([skill])
                        ).limit(2).all()
                        for r in resource_list:
                            resource_dict = r.to_dict()
                            # Ensure YouTube URL if not present
                            if not resource_dict.get('url') or 'youtube' not in resource_dict.get('url', '').lower():
                                import urllib.parse
                                skill_encoded = urllib.parse.quote(f"{skill} tutorial")
                                resource_dict['url'] = f"https://www.youtube.com/results?search_query={skill_encoded}"
                                resource_dict['provider'] = 'YouTube'
                                resource_dict['resource_type'] = 'video'
                            resource_dict['missing_skill'] = skill
                            # Avoid duplicates
                            if not any(res.get('id') == resource_dict.get('id') for res in resources):
                                resources.append(resource_dict)
                    
                    if resources:
                        response['message'] = f"I found {len(resources)} learning resources for your target role {user.target_role}. Here are the best tutorials:"
                        response['data'] = {'learning_resources': resources[:10]}
                        response['suggestions'] = [
                            "Get learning roadmap",
                            "Show more resources",
                            "Create study schedule",
                            "Get skill verification quiz"
                        ]
                    else:
                        response['message'] = f"To become a {user.target_role}, focus on learning: {', '.join(skill_gap['missing_skills'][:5])}. Would you like a structured learning roadmap?"
                        response['suggestions'] = ["Get learning roadmap", "Find resources", "Update my profile", "Get career advice"]
                else:
                    response['message'] = "I can help you find learning resources! What specific skill or topic would you like to learn about?"
                    response['suggestions'] = ["Database", "React", "Python", "Machine Learning"]
        else:
            response['message'] = "I can help you find learning resources! What specific skill or topic would you like to learn about? (e.g., 'database', 'react', 'python')"
            response['suggestions'] = ["Database", "React", "Python", "Machine Learning", "Get career recommendations"]
    
    elif intent == 'recommendation_explanation':
        # Explain why a recommendation was made
        feature_importance = ml_service.get_feature_importance()
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
        
        explanation = "Your recommendations are based on: "
        explanation += ", ".join([f"{feat.replace('skill_', '')} ({imp:.2%})" for feat, imp in top_features])
        
        response['message'] = explanation
        response['data'] = {'feature_importance': dict(top_features)}
    
    else:  # general_info
        # More interactive general responses
        if 'hello' in message.lower() or 'hi' in message.lower():
            response['message'] = f"Hello {user.full_name or user.username}! 👋 I'm your career guidance assistant. I can help you with:\n• Career recommendations\n• Job search\n• Skill gap analysis\n• Learning paths\n• Resume tips\n\nWhat would you like to explore today?"
        elif 'help' in message.lower():
            response['message'] = "I can help you with:\n\n📊 **Career Guidance**: Get personalized career recommendations\n💼 **Job Search**: Find jobs matching your skills\n📈 **Skill Analysis**: See what skills you need for your target role\n📚 **Learning Paths**: Get resources to close skill gaps\n📝 **Resume Help**: Upload your resume for analysis\n\nWhat would you like to do?"
        else:
            response['message'] = "I'm a career guidance assistant. I can help you with career advice, job search, skill gap analysis, and learning paths. What would you like to know?"
        
        response['suggestions'] = [
            "Get career recommendations",
            "Find jobs",
            "Analyze my skills",
            "Show learning resources"
        ]
    
    return jsonify(response), 200

def _extract_skill_from_message(message: str) -> str:
    """Extract skill/topic name from user message"""
    import re
    
    message_lower = message.lower()
    
    # Common patterns for requesting learning resources
    patterns = [
        r'(?:learning\s+resources?|resources?|tutorials?|courses?|learn|study|teach\s+me)\s+(?:for|about|on|regarding)?\s+([a-z\s]+?)(?:\s|$|\.|,|\?)',
        r'(?:show\s+me|give\s+me|find|get|search\s+for)\s+(?:learning\s+resources?|resources?|tutorials?|courses?)\s+(?:for|about|on)?\s+([a-z\s]+?)(?:\s|$|\.|,|\?)',
        r'(?:i\s+want\s+to\s+learn|i\s+need\s+to\s+learn|help\s+me\s+learn|teach\s+me)\s+([a-z\s]+?)(?:\s|$|\.|,|\?)',
        r'(?:how\s+to\s+learn|how\s+can\s+i\s+learn)\s+([a-z\s]+?)(?:\s|$|\.|,|\?)',
    ]
    
    # Common tech skills to look for
    tech_skills = [
        'database', 'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
        'react', 'angular', 'vue', 'javascript', 'typescript', 'node.js', 'node',
        'python', 'java', 'c++', 'c#', 'go', 'rust', 'php', 'ruby',
        'django', 'flask', 'spring', 'express', 'laravel',
        'machine learning', 'ml', 'deep learning', 'ai', 'artificial intelligence',
        'data science', 'data analysis', 'tensorflow', 'pytorch', 'keras',
        'aws', 'azure', 'gcp', 'cloud computing', 'docker', 'kubernetes',
        'devops', 'ci/cd', 'git', 'linux', 'bash', 'shell scripting',
        'html', 'css', 'bootstrap', 'tailwind', 'sass',
        'agile', 'scrum', 'project management'
    ]
    
    # Try pattern matching first
    for pattern in patterns:
        match = re.search(pattern, message_lower, re.IGNORECASE)
        if match:
            extracted = match.group(1).strip()
            # Clean up common words
            extracted = re.sub(r'\b(for|about|on|regarding|the|a|an)\b', '', extracted, flags=re.IGNORECASE).strip()
            if extracted and len(extracted) > 2:
                return extracted
    
    # Try direct skill matching
    for skill in tech_skills:
        # Look for skill as a word (not part of another word)
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, message_lower, re.IGNORECASE):
            return skill
    
    # Try to extract any technical term (2-3 words, lowercase)
    # Look for phrases after common request words
    request_words = ['for', 'about', 'on', 'regarding', 'learn', 'study', 'teach']
    for word in request_words:
        pattern = rf'\b{word}\s+([a-z]+(?:\s+[a-z]+)?)'
        match = re.search(pattern, message_lower)
        if match:
            extracted = match.group(1).strip()
            if extracted and 2 <= len(extracted) <= 30:
                return extracted
    
    return None

