"""
Analytics and unique features routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, CareerRole, QuizResult
from app.services.ml_service import ml_service
from app.utils.auth_helpers import get_current_user_id
from app.utils.role_helpers import find_role_by_name, get_available_roles

bp = Blueprint('analytics', __name__)

@bp.route('/roadmap', methods=['GET'])
@jwt_required()
def get_roadmap():
    """Get learning roadmap for a specific skill"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    skill = request.args.get('skill', '').strip()
    
    if not skill:
        return jsonify({'error': 'Skill parameter is required'}), 400
    
    try:
        from app.services.learning_roadmap_service import LearningRoadmapService
        roadmap_service = LearningRoadmapService()
        roadmap = roadmap_service.generate_roadmap_for_skill(
            skill,
            user.skills or []
        )
        
        # Enhance roadmap with beginner to advanced progression
        roadmap['progression_levels'] = _get_progression_levels(roadmap)
        
        return jsonify(roadmap), 200
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        return jsonify({'error': f'Failed to generate roadmap: {str(e)}'}), 500

def _get_progression_levels(roadmap: dict) -> list:
    """Get beginner to advanced progression levels"""
    total_weeks = roadmap.get('total_weeks', 0)
    weeks = roadmap.get('weeks', [])
    
    if total_weeks == 0:
        return []
    
    # Divide into beginner, intermediate, advanced
    beginner_weeks = max(1, total_weeks // 3)
    intermediate_weeks = max(1, total_weeks // 3)
    advanced_weeks = total_weeks - beginner_weeks - intermediate_weeks
    
    levels = []
    
    # Beginner level
    if beginner_weeks > 0:
        beginner_week_data = weeks[:beginner_weeks]
        levels.append({
            'level': 'beginner',
            'title': 'Beginner',
            'description': 'Learn the fundamentals and basics',
            'weeks': beginner_week_data,
            'total_hours': sum(w.get('hours', 0) for w in beginner_week_data),
            'icon': '🌱'
        })
    
    # Intermediate level
    if intermediate_weeks > 0:
        intermediate_week_data = weeks[beginner_weeks:beginner_weeks + intermediate_weeks]
        levels.append({
            'level': 'intermediate',
            'title': 'Intermediate',
            'description': 'Build on fundamentals with practical projects',
            'weeks': intermediate_week_data,
            'total_hours': sum(w.get('hours', 0) for w in intermediate_week_data),
            'icon': '🚀'
        })
    
    # Advanced level
    if advanced_weeks > 0:
        advanced_week_data = weeks[beginner_weeks + intermediate_weeks:]
        levels.append({
            'level': 'advanced',
            'title': 'Advanced',
            'description': 'Master advanced concepts and best practices',
            'weeks': advanced_week_data,
            'total_hours': sum(w.get('hours', 0) for w in advanced_week_data),
            'icon': '⭐'
        })
    
    return levels

@bp.route('/career-path-simulator', methods=['GET'])
@jwt_required()
def get_career_path():
    """Get career path simulator for target role"""
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
    
    # Define career progression path
    typical_path = target_role.typical_path or [
        {'level': 'Junior', 'years': 0, 'skills': []},
        {'level': 'Mid', 'years': 2, 'skills': []},
        {'level': 'Senior', 'years': 5, 'skills': []},
        {'level': 'Lead/Architect', 'years': 8, 'skills': []}
    ]
    
    # Analyze current position
    current_experience = user.experience_years or 0
    skill_gap = ml_service.analyze_skill_gap(
        user.skills or [],
        target_role.required_skills or []
    )
    
    # Calculate time to reach each level
    career_path = []
    for i, level in enumerate(typical_path):
        years_needed = max(0, level['years'] - current_experience)
        
        # Estimate time based on skill gap
        if i == 0:  # Junior level
            skill_gap_pct = skill_gap['gap_percentage']
            estimated_months = max(3, int(skill_gap_pct / 10))  # Rough estimate
        else:
            estimated_months = max(6, years_needed * 12)
        
        career_path.append({
            'level': level['level'],
            'years_experience_required': level['years'],
            'years_from_current': years_needed,
            'estimated_time_to_reach': f"{estimated_months} months",
            'required_skills': level.get('skills', [])
        })
    
    return jsonify({
        'target_role': target_role.to_dict(),
        'current_experience': current_experience,
        'current_skill_match': skill_gap['match_percentage'],
        'career_path': career_path
    }), 200

@bp.route('/trust-panel', methods=['GET'])
@jwt_required()
def get_trust_panel():
    """Get trust and transparency panel data"""
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
    
    # Get feature importance
    feature_importance = ml_service.get_feature_importance()
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Analyze skill gap
    skill_gap = ml_service.analyze_skill_gap(
        user.skills or [],
        target_role.required_skills or []
    )
    
    # Get user features for recommendation
    user_features = {
        'skills': user.skills or [],
        'experience_years': user.experience_years or 0,
        'current_role': user.current_role or '',
        'interests': user.interests or []
    }
    
    # Get recommendations to explain
    recommendations = ml_service.get_hybrid_recommendations(user_features, top_k=1)
    
    explanation = {
        'target_role': target_role.to_dict(),
        'top_influencing_factors': [
            {
                'factor': feat.replace('skill_', '').replace('_', ' ').title(),
                'importance': round(imp * 100, 2),
                'user_has': any(feat.replace('skill_', '').lower() in str(s).lower() for s in (user.skills or []))
            }
            for feat, imp in top_features[:5]
        ],
        'skill_analysis': {
            'matching_skills': skill_gap['matching_skills'],
            'missing_skills': skill_gap['missing_skills'],
            'match_percentage': skill_gap['match_percentage']
        },
        'recommendation_score': recommendations['roles'][0].get('score', 0) if recommendations['roles'] else 0
    }
    
    return jsonify(explanation), 200

@bp.route('/quiz/submit', methods=['POST'])
@jwt_required()
def submit_quiz():
    """Submit quiz results"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    if not data or not data.get('skill') or not data.get('score'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    quiz_result = QuizResult(
        user_id=user_id,
        skill=data['skill'],
        score=data['score'],
        total_questions=data.get('total_questions', 10),
        correct_answers=data.get('correct_answers', 0)
    )
    
    try:
        db.session.add(quiz_result)
        
        # Update user skills based on quiz score
        user = User.query.get(user_id)
        if user:
            skills = user.skills or []
            skill_name = data['skill']
            
            # Update or add skill proficiency
            skill_found = False
            for i, skill in enumerate(skills):
                if isinstance(skill, dict) and skill.get('name') == skill_name:
                    skills[i]['proficiency'] = data['score'] / 100
                    skill_found = True
                    break
                elif isinstance(skill, str) and skill.lower() == skill_name.lower():
                    skills[i] = {'name': skill_name, 'proficiency': data['score'] / 100}
                    skill_found = True
                    break
            
            if not skill_found:
                skills.append({'name': skill_name, 'proficiency': data['score'] / 100})
            
            user.skills = skills
            db.session.commit()
        
        return jsonify({
            'message': 'Quiz result submitted successfully',
            'quiz_result': quiz_result.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    """Get system metrics (admin/diagnostics)"""
    from app.models import User, Job, CareerRole, Feedback
    
    metrics = {
        'total_users': User.query.count(),
        'total_jobs': Job.query.count(),
        'total_roles': CareerRole.query.count(),
        'total_feedback': Feedback.query.count()
    }
    
    return jsonify(metrics), 200

