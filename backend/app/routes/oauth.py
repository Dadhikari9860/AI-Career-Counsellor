"""
Google OAuth routes
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token
import os

# Try to import Google OAuth libraries (optional)
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests
    GOOGLE_OAUTH_AVAILABLE = True
except ImportError:
    GOOGLE_OAUTH_AVAILABLE = False
    print("Warning: Google OAuth libraries not installed. Google login will be disabled.")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2")

bp = Blueprint('oauth', __name__)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')

@bp.route('/auth/google/config', methods=['GET'])
def google_config():
    """Get Google OAuth configuration for frontend"""
    return jsonify({
        'client_id': GOOGLE_CLIENT_ID,
        'enabled': bool(GOOGLE_CLIENT_ID and GOOGLE_OAUTH_AVAILABLE)
    }), 200

@bp.route('/auth/google/verify', methods=['POST'])
def verify_google_token():
    """Verify Google ID token from Google Sign-In"""
    if not GOOGLE_OAUTH_AVAILABLE:
        return jsonify({
            'error': 'Google OAuth not available',
            'message': 'Please install: pip install google-auth google-auth-oauthlib google-auth-httplib2'
        }), 500
    
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token not provided'}), 400
        
        if not GOOGLE_CLIENT_ID:
            return jsonify({
                'error': 'Google OAuth not configured',
                'message': 'Please set GOOGLE_CLIENT_ID environment variable'
            }), 500
        
        # Verify the token
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_CLIENT_ID
            )
            
            # Check issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            email = idinfo.get('email')
            name = idinfo.get('name', '')
            google_id = idinfo.get('sub')
            picture = idinfo.get('picture', '')
            
            if not email:
                return jsonify({'error': 'Email not provided by Google'}), 400
            
            # Find or create user
            user = User.query.filter_by(email=email).first()
            
            if not user:
                # Create new user
                username = email.split('@')[0]
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=email,
                    full_name=name,
                    password_hash='google_oauth'  # Placeholder, won't be used for Google users
                )
                db.session.add(user)
                db.session.commit()
            
            # Create JWT token
            access_token = create_access_token(identity=str(user.id))
            
            return jsonify({
                'message': 'Google login successful',
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
            
        except ValueError as e:
            print(f"Token verification error: {e}")
            return jsonify({'error': f'Invalid token: {str(e)}'}), 400
            
    except Exception as e:
        import traceback
        print(f"Google token verification error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': 'Token verification failed'}), 500

