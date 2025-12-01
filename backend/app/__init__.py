from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = config_class.SECRET_KEY  # For session management
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        # Log the error for debugging
        import traceback
        print(f"JWT Invalid Token Error: {str(error)}")
        print(traceback.format_exc())
        return {'error': f'Invalid token: {str(error)}'}, 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization header is missing'}, 401
    
    # Add a before_request handler to debug token issues
    @app.before_request
    def log_request_info():
        from flask import request
        if request.path.startswith('/api') and request.method != 'OPTIONS':
            auth_header = request.headers.get('Authorization', 'Not provided')
            print(f"Request: {request.method} {request.path}")
            print(f"Authorization: {auth_header[:50] if len(auth_header) > 50 else auth_header}")
    
    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.recommendations import bp as recommendations_bp
    from app.routes.chatbot import bp as chatbot_bp
    from app.routes.feedback import bp as feedback_bp
    from app.routes.profile import bp as profile_bp
    from app.routes.analytics import bp as analytics_bp
    from app.routes.roles import bp as roles_bp
    from app.routes.resume import bp as resume_bp
    from app.routes.oauth import bp as oauth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(recommendations_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    app.register_blueprint(roles_bp, url_prefix='/api')
    app.register_blueprint(resume_bp, url_prefix='/api')
    app.register_blueprint(oauth_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

