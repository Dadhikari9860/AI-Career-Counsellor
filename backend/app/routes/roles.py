"""
Roles routes - Get available roles
"""

from flask import Blueprint, jsonify
from app.models import CareerRole

bp = Blueprint('roles', __name__)

@bp.route('/roles', methods=['GET'])
def get_roles():
    """Get all available career roles"""
    roles = CareerRole.query.all()
    return jsonify({
        'roles': [role.to_dict() for role in roles]
    }), 200

