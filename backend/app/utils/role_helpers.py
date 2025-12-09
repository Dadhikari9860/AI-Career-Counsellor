"""
Helper functions for role matching
"""

from app.models import CareerRole

def find_role_by_name(role_name):
    """
    Find a career role by name with flexible matching
    Returns the role or None if not found
    """
    if not role_name:
        return None
    
    # Try exact match first
    role = CareerRole.query.filter_by(title=role_name).first()
    if role:
        return role
    
    # Try case-insensitive match
    role = CareerRole.query.filter(
        CareerRole.title.ilike(f'%{role_name}%')
    ).first()
    if role:
        return role
    
    # Try matching common variations
    role_variations = {
        'fullstack developer': 'Full Stack Developer',
        'full stack developer': 'Full Stack Developer',
        'fullstack': 'Full Stack Developer',
        'full-stack developer': 'Full Stack Developer',
        'full-stack': 'Full Stack Developer',
        'full stack': 'Full Stack Developer',
        'data scientist': 'Data Scientist',
        'data science': 'Data Scientist',
        'ml engineer': 'ML Engineer',
        'machine learning engineer': 'ML Engineer',
        'machine learning': 'ML Engineer',
        'ml': 'ML Engineer',
        'software engineer': 'Software Engineer',
        'software developer': 'Software Engineer',
        'swe': 'Software Engineer',
        'backend developer': 'Backend Developer',
        'backend': 'Backend Developer',
        'back-end developer': 'Backend Developer',
        'frontend developer': 'Frontend Developer',
        'frontend': 'Frontend Developer',
        'front-end developer': 'Frontend Developer',
        'devops engineer': 'DevOps Engineer',
        'devops': 'DevOps Engineer',
        'dev ops': 'DevOps Engineer',
        'dev-ops': 'DevOps Engineer',
        'product manager': 'Product Manager',
        'pm': 'Product Manager',
        'ux designer': 'UX Designer',
        'ux': 'UX Designer',
        'ui/ux': 'UX Designer',
        'data analyst': 'Data Analyst',
        'analyst': 'Data Analyst',
        'web developer': 'Full Stack Developer',
        'react developer': 'Frontend Developer',
        'python developer': 'Software Engineer',
        'java developer': 'Software Engineer',
        'cloud engineer': 'DevOps Engineer',
        'cloud architect': 'DevOps Engineer'
    }
    
    normalized = role_name.lower().strip()
    if normalized in role_variations:
        role = CareerRole.query.filter_by(title=role_variations[normalized]).first()
        if role:
            return role
    
    return None

def get_available_roles():
    """Get list of all available career roles"""
    return [r.title for r in CareerRole.query.all()]

