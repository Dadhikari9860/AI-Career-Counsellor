"""
Recommendation routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, Job, CareerRole, LearningResource
from app.services.ml_service import ml_service
from app.utils.auth_helpers import get_current_user_id
from app.utils.role_helpers import find_role_by_name, get_available_roles
import urllib.parse

bp = Blueprint('recommendations', __name__)

@bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get hybrid recommendations for the current user"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    top_k = request.args.get('top_k', 10, type=int)
    
    # Prepare user features
    user_features = {
        'user_id': user_id,
        'skills': user.skills or [],
        'experience_years': user.experience_years or 0,
        'current_role': user.current_role or '',
        'interests': user.interests or []
    }
    
    # Get ML recommendations
    ml_results = ml_service.get_hybrid_recommendations(user_features, top_k=top_k)
    
    # Fetch full details from database
    recommendations = {
        'roles': [],
        'jobs': [],
        'resources': []
    }
    
    # Get role recommendations (with deduplication)
    seen_role_ids = set()
    seen_role_titles = set()
    
    for rec in ml_results['roles'][:top_k]:
        role_id = rec.get('role_id')
        role_name = rec.get('role')
        
        # Skip if we've already added this role
        if role_id and role_id in seen_role_ids:
            continue
        if role_name and role_name.lower() in seen_role_titles:
            continue
        
        if role_id:
            role = CareerRole.query.get(role_id)
            if role:
                role_dict = role.to_dict()
                role_dict['score'] = rec.get('hybrid_score', rec.get('score', 0))
                role_dict['method'] = rec.get('method', 'hybrid')
                recommendations['roles'].append(role_dict)
                seen_role_ids.add(role_id)
                seen_role_titles.add(role.title.lower() if role.title else '')
        elif role_name:
            role = CareerRole.query.filter_by(title=role_name).first()
            if role:
                role_dict = role.to_dict()
                role_dict['score'] = rec.get('hybrid_score', rec.get('score', 0))
                role_dict['method'] = rec.get('method', 'hybrid')
                recommendations['roles'].append(role_dict)
                seen_role_ids.add(role.id)
                seen_role_titles.add(role_name.lower())
    
    # Get job recommendations from database
    target_role = user.target_role or user.current_role or 'Software Engineer'
    for rec in ml_results['jobs'][:top_k]:
        job_id = rec.get('job_id')
        if job_id:
            job = Job.query.get(job_id)
            if job:
                job_dict = job.to_dict()
                job_dict['score'] = rec.get('score', 0)
                job_dict['match_score'] = rec.get('score', 0)
                job_dict['method'] = rec.get('method', 'content_based')
                # Ensure LinkedIn URL - always provide a link
                if not job_dict.get('url'):
                    from app.services.job_scraper import JobScraper
                    scraper = JobScraper()
                    job_title = job_dict.get('title') or target_role
                    job_dict['url'] = scraper.get_linkedin_search_url(job_title)
                recommendations['jobs'].append(job_dict)
    
    # Also get real-time LinkedIn jobs based on user skills and location (personalized)
    try:
        from app.services.job_scraper import JobScraper
        scraper = JobScraper()
        # Normalize skills to strings
        user_skills = [str(s).strip() if isinstance(s, str) else str(s.get('name', '')).strip() 
                      for s in (user.skills or []) if s]
        # Remove empty skills
        user_skills = [s for s in user_skills if s]
        
        target_role = user.target_role or user.current_role or 'Software Engineer'
        user_location = user.location or ""  # Get user's location from profile
        
        print(f"Getting personalized job recommendations for user {user_id} with {len(user_skills)} skills: {user_skills[:5]}")
        linkedin_jobs = scraper.get_jobs_for_user(user_skills, target_role, user_location)
        
        # Add LinkedIn jobs to recommendations (prioritize them)
        for job in linkedin_jobs[:5]:
            # Ensure job has proper LinkedIn URL with location
            if not job.get('url') or 'linkedin.com' not in job.get('url', ''):
                job['url'] = scraper.get_linkedin_search_url(target_role, user_location)
            
            # Avoid duplicates
            if not any(j.get('title') == job.get('title') and j.get('company') == job.get('company') 
                      for j in recommendations['jobs']):
                recommendations['jobs'].insert(0, job)  # Insert at beginning
        
        # Add LinkedIn profile search URL to recommendations
        if user_location or user.full_name or user.current_role:
            recommendations['linkedin_profile_url'] = scraper.get_linkedin_profile_search_url(
                full_name=user.full_name or user.username,
                location=user_location,
                current_role=user.current_role or target_role
            )
    except Exception as e:
        print(f"Error getting LinkedIn jobs: {e}")
        # Continue without LinkedIn jobs
    
    # Get learning resources (based on skill gaps) with YouTube links
    if user.target_role:
        target_role = find_role_by_name(user.target_role)
        if target_role:
            skill_gap = ml_service.analyze_skill_gap(
                user.skills or [],
                target_role.required_skills or []
            )
            
            # Get YouTube resources for missing skills
            try:
                from app.services.youtube_learning_service import YouTubeLearningService
                youtube_service = YouTubeLearningService()
                youtube_resources = youtube_service.get_learning_resources_for_skill_gap(
                    skill_gap['missing_skills'][:10], 
                    limit_per_skill=2
                )
                
                # Add YouTube resources (prioritize them)
                for resource in youtube_resources:
                    recommendations['resources'].append(resource)
            except Exception as e:
                print(f"Error getting YouTube resources: {e}")
            
            # Also find resources from database
            for skill in skill_gap['missing_skills'][:10]:
                resources = LearningResource.query.filter(
                    LearningResource.skills_covered.contains([skill])
                ).limit(2).all()
                
                for resource in resources:
                    resource_dict = resource.to_dict()
                    # Ensure resource has a URL - if not, create a YouTube search URL
                    if not resource_dict.get('url'):
                        # Create a YouTube search URL for the skill
                        skill_encoded = urllib.parse.quote(f"{skill} tutorial")
                        resource_dict['url'] = f"https://www.youtube.com/results?search_query={skill_encoded}"
                    resource_dict['missing_skill'] = skill  # Tag which skill it addresses
                    # Avoid duplicates
                    if not any(r.get('id') == resource_dict.get('id') for r in recommendations['resources']):
                        recommendations['resources'].append(resource_dict)
            
            # If no resources found, create YouTube-based resources for missing skills
            if not recommendations['resources']:
                try:
                    from app.services.youtube_learning_service import YouTubeLearningService
                    youtube_service = YouTubeLearningService()
                    youtube_resources = youtube_service.get_learning_resources_for_skill_gap(
                        skill_gap['missing_skills'][:5], 
                        limit_per_skill=1
                    )
                    recommendations['resources'].extend(youtube_resources)
                except Exception as e:
                    print(f"Error getting YouTube resources: {e}")
                    # Fallback to generic search
                    for skill in skill_gap['missing_skills'][:5]:
                        skill_encoded = urllib.parse.quote(f"{skill} tutorial")
                        recommendations['resources'].append({
                            'id': f"youtube_{skill}",
                            'title': f"Learn {skill} - YouTube Tutorials",
                            'description': f"Find the best YouTube tutorials to learn {skill} for {target_role.title}",
                            'url': f"https://www.youtube.com/results?search_query={skill_encoded}",
                            'resource_type': 'video',
                            'provider': 'YouTube',
                            'skills_covered': [skill],
                            'missing_skill': skill,
                            'source': 'youtube'
                        })
    
    return jsonify(recommendations), 200

@bp.route('/skill-gap', methods=['GET'])
@jwt_required()
def get_skill_gap():
    """Get skill gap analysis for current user"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    target_role_name = request.args.get('target_role') or user.target_role
    
    if not target_role_name:
        return jsonify({'error': 'No target role specified'}), 400
    
    target_role = find_role_by_name(target_role_name)
    
    if not target_role:
        return jsonify({
            'error': f'Target role "{target_role_name}" not found',
            'suggestions': get_available_roles(),
            'message': 'Please use one of the available roles or set a target role in your profile'
        }), 404
    
    # Analyze skill gap
    skill_gap = ml_service.analyze_skill_gap(
        user.skills or [],
        target_role.required_skills or []
    )
    
    # Get learning resources for missing skills (including YouTube)
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
    for skill in skill_gap['missing_skills'][:10]:
        resource_list = LearningResource.query.filter(
            LearningResource.skills_covered.contains([skill])
        ).limit(2).all()
        
        for resource in resource_list:
            if resource.id not in [r.get('id') for r in resources]:
                resource_dict = resource.to_dict()
                # Ensure YouTube URL if not present
                if not resource_dict.get('url') or 'youtube' not in resource_dict.get('url', '').lower():
                    skill_encoded = urllib.parse.quote(f"{skill} tutorial")
                    resource_dict['url'] = f"https://www.youtube.com/results?search_query={skill_encoded}"
                    resource_dict['provider'] = 'YouTube'
                    resource_dict['resource_type'] = 'video'
                # Ensure resource has a URL
                if not resource_dict.get('url'):
                    skill_encoded = skill.replace(' ', '+')
                    resource_dict['url'] = f"https://www.google.com/search?q=learn+{skill_encoded}+tutorial+course"
                resource_dict['missing_skill'] = skill
                resources.append(resource_dict)
    
    # If no resources in DB, create placeholder resources
    if not resources:
        for skill in skill_gap['missing_skills'][:5]:
            resources.append({
                'id': f"placeholder_{skill}",
                'title': f"Learn {skill}",
                'description': f"Resources to help you learn {skill} for {target_role.title}",
                'url': f"https://www.google.com/search?q=learn+{skill.replace(' ', '+')}+tutorial+course+free",
                'type': 'course',
                'skills_covered': [skill],
                'missing_skill': skill
            })
    
    return jsonify({
        'target_role': target_role.to_dict(),
        'skill_gap': skill_gap,
        'learning_resources': resources
    }), 200

@bp.route('/learning-path', methods=['GET'])
@jwt_required()
def get_learning_path():
    """Get learning path to close skill gap"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    target_role_name = request.args.get('target_role') or user.target_role
    
    if not target_role_name:
        return jsonify({'error': 'No target role specified'}), 400
    
    target_role = find_role_by_name(target_role_name)
    
    if not target_role:
        return jsonify({
            'error': f'Target role "{target_role_name}" not found',
            'suggestions': get_available_roles(),
            'message': 'Please use one of the available roles or set a target role in your profile'
        }), 404
    
    # Analyze skill gap
    skill_gap = ml_service.analyze_skill_gap(
        user.skills or [],
        target_role.required_skills or []
    )
    
    # Create ordered learning path
    learning_path = []
    for skill in skill_gap['missing_skills']:
        resources = LearningResource.query.filter(
            LearningResource.skills_covered.contains([skill])
        ).order_by(LearningResource.difficulty_level).all()
        
        if resources:
            learning_path.append({
                'skill': skill,
                'resources': [r.to_dict() for r in resources[:3]],
                'estimated_time': _estimate_learning_time(resources)
            })
    
    return jsonify({
        'target_role': target_role.to_dict(),
        'learning_path': learning_path,
        'total_skills_to_learn': len(skill_gap['missing_skills'])
    }), 200

def _estimate_learning_time(resources):
    """Estimate total learning time from resources"""
    import re
    total_hours = 0
    for resource in resources:
        duration = resource.duration or ''
        # Extract hours from duration string
        hours_match = re.search(r'(\d+)\s*hours?', duration.lower())
        if hours_match:
            total_hours += int(hours_match.group(1))
        else:
            # Default estimate
            total_hours += 10
    
    return f"{total_hours} hours"

