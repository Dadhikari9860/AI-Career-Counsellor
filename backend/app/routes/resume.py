"""
Resume upload and parsing routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from app import db
from app.models import User
from app.services.resume_parser import ResumeParser
from app.services.job_scraper import JobScraper
from app.utils.auth_helpers import get_current_user_id
from config import Config

bp = Blueprint('resume', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
UPLOAD_FOLDER = 'uploads/resumes'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/resume/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    """Upload and parse resume"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if 'resume' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PDF, DOC, DOCX, TXT'}), 400
    
    try:
        # Create upload directory
        upload_path = Path(UPLOAD_FOLDER)
        upload_path.mkdir(parents=True, exist_ok=True)
        
        # Save file
        filename = secure_filename(f"{user_id}_{file.filename}")
        file_path = upload_path / filename
        
        try:
            file.save(str(file_path))
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
        
        # Parse resume
        try:
            parser = ResumeParser()
            parsed_data = parser.parse_resume(str(file_path))
        except Exception as e:
            # Clean up file
            if file_path.exists():
                try:
                    file_path.unlink()
                except:
                    pass
            return jsonify({'error': f'Failed to parse resume: {str(e)}'}), 500
        
        if 'error' in parsed_data:
            # Clean up file
            if file_path.exists():
                try:
                    file_path.unlink()
                except:
                    pass
            return jsonify({'error': parsed_data['error']}), 400
        
        # Update user profile with parsed data
        if parsed_data.get('skills'):
            # Merge with existing skills
            existing_skills = user.skills or []
            existing_skill_names = [s if isinstance(s, str) else s.get('name', '') for s in existing_skills]
            
            new_skills = []
            for skill in parsed_data['skills']:
                if skill not in existing_skill_names:
                    new_skills.append(skill)
            
            user.skills = existing_skills + new_skills
        
        if parsed_data.get('experience_years') and parsed_data['experience_years'] > (user.experience_years or 0):
            user.experience_years = parsed_data['experience_years']
        
        if parsed_data.get('education'):
            user.education = parsed_data['education']
        
        if parsed_data.get('current_role') and not user.current_role:
            user.current_role = parsed_data['current_role']
        
        # Update location from resume if extracted
        if parsed_data.get('location') and not user.location:
            user.location = parsed_data['location']
        elif parsed_data.get('location'):
            # Update location if resume has a more specific one
            user.location = parsed_data['location']
        
        db.session.commit()
        
        # Get job recommendations based on resume (use location and skills from resume)
        recommended_jobs = []
        try:
            scraper = JobScraper()
            # Prioritize skills from parsed resume, then user profile
            resume_skills = parsed_data.get('skills', [])
            profile_skills = [s if isinstance(s, str) else s.get('name', '') for s in (user.skills or [])]
            # Combine and deduplicate skills (resume skills first)
            all_skills = resume_skills + [s for s in profile_skills if s not in resume_skills]
            # Normalize skills to strings
            user_skills = [str(s).strip() for s in all_skills if s and str(s).strip()]
            
            target_role = user.target_role or parsed_data.get('current_role') or 'Software Engineer'
            # Use location from resume (parsed_data) or user profile
            user_location = parsed_data.get('location') or user.location or ""
            
            print(f"Getting personalized job recommendations for user with {len(user_skills)} skills: {user_skills[:5]}")
            recommended_jobs = scraper.get_jobs_for_user(user_skills, target_role, user_location)
            
            # Generate LinkedIn profile search link based on resume data
            linkedin_profile_url = scraper.get_linkedin_profile_search_url(
                full_name=user.full_name or (parsed_data.get('email', '').split('@')[0] if parsed_data.get('email') else user.username),
                location=user_location,
                current_role=parsed_data.get('current_role') or user.current_role or ''
            )
            
            # Add LinkedIn profile link to parsed data
            parsed_data['linkedin_profile_url'] = linkedin_profile_url
            
            # Ensure all recommended jobs have proper LinkedIn URLs with location
            for job in recommended_jobs:
                if not job.get('url') or 'linkedin.com' not in job.get('url', ''):
                    job['url'] = scraper.get_linkedin_search_url(
                        job.get('title', target_role),
                        user_location
                    )
        except Exception as e:
            print(f"Error getting job recommendations: {e}")
            # Continue without job recommendations
        
        # Clean up file after processing
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Error deleting file: {e}")
        
        return jsonify({
            'message': 'Resume parsed successfully',
            'parsed_data': parsed_data,
            'user_updated': user.to_dict(),
            'recommended_jobs': recommended_jobs[:5],
            'linkedin_profile_url': parsed_data.get('linkedin_profile_url'),
            'suggestions': [
                'Update your profile with extracted information',
                'View recommended jobs',
                'Check skill gaps',
                'Get learning path'
            ]
        }), 200
        
    except Exception as e:
        # Clean up file on error
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        return jsonify({'error': f'Failed to process resume: {str(e)}'}), 500

@bp.route('/resume/analyze', methods=['POST'])
@jwt_required()
def analyze_resume_text():
    """Analyze resume text directly (for paste/input)"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    
    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400
    
    try:
        # Parse resume text
        parser = ResumeParser()
        parsed_data = parser._extract_info(resume_text)
        
        # Get job recommendations (use location and skills from parsed data or user profile)
        scraper = JobScraper()
        # Get skills from parsed data and user profile
        resume_skills = parsed_data.get('skills', [])
        profile_skills = [s if isinstance(s, str) else s.get('name', '') for s in (user.skills or [])]
        # Combine and deduplicate skills (resume skills first)
        all_skills = resume_skills + [s for s in profile_skills if s not in resume_skills]
        # Normalize skills to strings
        user_skills = [str(s).strip() for s in all_skills if s and str(s).strip()]
        
        target_role = user.target_role or parsed_data.get('current_role') or 'Software Engineer'
        user_location = parsed_data.get('location') or user.location or ""  # Use location from resume first
        
        print(f"Getting personalized job recommendations for user with {len(user_skills)} skills: {user_skills[:5]}")
        recommended_jobs = scraper.get_jobs_for_user(user_skills, target_role, user_location)
        
        # Generate LinkedIn profile search link
        linkedin_profile_url = scraper.get_linkedin_profile_search_url(
            full_name=user.full_name or user.username,
            location=user_location,
            current_role=parsed_data.get('current_role') or user.current_role or ''
        )
        parsed_data['linkedin_profile_url'] = linkedin_profile_url
        
        # Ensure all recommended jobs have proper LinkedIn URLs with location
        for job in recommended_jobs:
            if not job.get('url') or 'linkedin.com' not in job.get('url', ''):
                job['url'] = scraper.get_linkedin_search_url(
                    job.get('title', target_role),
                    user_location
                )
        
        return jsonify({
            'message': 'Resume analyzed successfully',
            'parsed_data': parsed_data,
            'recommended_jobs': recommended_jobs[:5],
            'linkedin_profile_url': linkedin_profile_url
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500

