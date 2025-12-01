"""
Profile routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import User
from app.utils.auth_helpers import get_current_user_id

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'location' in data:
        user.location = data['location']
    if 'skills' in data:
        user.skills = data['skills']
    if 'experience_years' in data:
        user.experience_years = data['experience_years']
    if 'education' in data:
        user.education = data['education']
    if 'interests' in data:
        user.interests = data['interests']
    if 'current_role' in data:
        user.current_role = data['current_role']
    if 'target_role' in data:
        user.target_role = data['target_role']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

