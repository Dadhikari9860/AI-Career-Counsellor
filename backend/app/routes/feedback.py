"""
Feedback routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Feedback
from app.utils.auth_helpers import get_current_user_id

bp = Blueprint('feedback', __name__)

@bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    """Submit feedback on recommendations"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    if not data or not data.get('item_type') or not data.get('item_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    feedback = Feedback(
        user_id=user_id,
        item_type=data['item_type'],  # 'job', 'role', 'resource'
        item_id=data['item_id'],
        rating=data.get('rating'),
        feedback_type=data.get('feedback_type', 'click')  # 'click', 'save', 'like', 'dislike'
    )
    
    try:
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback': feedback.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

