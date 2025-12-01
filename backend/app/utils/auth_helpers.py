"""
Authentication helper functions
"""

from flask_jwt_extended import get_jwt_identity

def get_current_user_id():
    """Get current user ID from JWT token and convert to int"""
    user_id = get_jwt_identity()
    # JWT identity is stored as string, convert to int
    return int(user_id) if user_id else None

