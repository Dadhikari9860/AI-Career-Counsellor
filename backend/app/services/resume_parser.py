"""
Resume parsing service - Extract skills, experience, education from resumes
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Optional
import PyPDF2
import pdfplumber
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

class ResumeParser:
    """Parse resume files to extract information"""
    
    def __init__(self):
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
            'aws', 'docker', 'kubernetes', 'git', 'linux', 'html', 'css',
            'machine learning', 'data science', 'tensorflow', 'pytorch',
            'agile', 'scrum', 'rest api', 'graphql', 'microservices',
            'typescript', 'angular', 'vue', 'django', 'flask', 'spring',
            'postgresql', 'mysql', 'redis', 'elasticsearch', 'kafka',
            'ci/cd', 'jenkins', 'terraform', 'ansible', 'nginx'
        ]
    
    def parse_resume(self, file_path: str) -> Dict:
        """Parse resume file and extract information"""
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.pdf':
                text = self._extract_from_pdf(file_path)
            elif file_ext == '.docx' and DOCX_AVAILABLE:
                text = self._extract_from_docx(file_path)
            elif file_ext in ['.txt', '.doc']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            else:
                return {'error': 'Unsupported file format'}
            
            return self._extract_info(text)
        except Exception as e:
            return {'error': f'Failed to parse resume: {str(e)}'}
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        
        # Try pdfplumber first (better for tables)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except:
            # Fallback to PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        doc = Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)
    
    def _extract_info(self, text: str) -> Dict:
        """Extract information from resume text"""
        text_lower = text.lower()
        
        # Extract skills
        skills = self._extract_skills(text_lower)
        
        # Extract experience years
        experience_years = self._extract_experience_years(text)
        
        # Extract education
        education = self._extract_education(text)
        
        # Extract current role
        current_role = self._extract_current_role(text)
        
        # Extract email
        email = self._extract_email(text)
        
        # Extract phone
        phone = self._extract_phone(text)
        
        # Extract location
        location = self._extract_location(text)
        
        return {
            'skills': skills,
            'experience_years': experience_years,
            'education': education,
            'current_role': current_role,
            'email': email,
            'phone': phone,
            'location': location,
            'raw_text': text[:1000]  # First 1000 chars for reference
        }
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        found_skills = []
        for skill in self.skill_keywords:
            # Check for skill mentions
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)
        
        # Also look for common patterns like "Skills:", "Technical Skills:", etc.
        skills_section = re.search(
            r'(?:skills?|technical\s+skills?|technologies?|tools?)[:]\s*(.+?)(?:\n\n|\n[A-Z]|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if skills_section:
            skills_text = skills_section.group(1)
            for skill in self.skill_keywords:
                if skill.lower() in skills_text.lower():
                    if skill not in found_skills:
                        found_skills.append(skill)
        
        return list(set(found_skills))
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract years of experience"""
        # Look for patterns like "5 years", "5+ years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Count job entries or positions
        job_count = len(re.findall(r'(?:worked|experience|position|role|job)', text, re.IGNORECASE))
        if job_count > 0:
            return min(job_count, 10)  # Cap at 10 years
        
        return 0
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            r'\b(bachelor|b\.?s\.?|b\.?tech|b\.?e\.?)\b',
            r'\b(master|m\.?s\.?|m\.?tech|m\.?e\.?|mba)\b',
            r'\b(ph\.?d|doctorate|doctoral)\b',
        ]
        
        for pattern in degree_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if 'bachelor' in pattern or r'b\.' in pattern:
                    education.append('Bachelor')
                elif 'master' in pattern or r'm\.' in pattern or 'mba' in pattern:
                    education.append('Master')
                elif 'ph' in pattern or 'doctorate' in pattern:
                    education.append('PhD')
        
        return list(set(education)) if education else ['Bachelor']  # Default
    
    def _extract_current_role(self, text: str) -> Optional[str]:
        """Extract current role/job title"""
        # Look for patterns like "Software Engineer", "Current Role:", etc.
        patterns = [
            r'(?:current\s+)?(?:position|role|title|job)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+\s+(?:Engineer|Developer|Scientist|Analyst|Manager|Designer|Architect))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                role = match.group(1).strip()
                if len(role) < 50:  # Reasonable role length
                    return role
        
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location from resume text - improved to avoid false positives"""
        # Words that indicate this is NOT a location (job descriptions, etc.)
        invalid_keywords = [
            'testing', 'deployment', 'development', 'design', 'implementation',
            'product', 'project', 'application', 'software', 'system',
            'responsibilities', 'duties', 'experience', 'skills', 'technologies',
            'framework', 'library', 'database', 'server', 'client', 'api',
            'ui', 'ux', 'frontend', 'backend', 'fullstack', 'devops'
        ]
        
        # Common location patterns - more strict
        location_patterns = [
            # Pattern: "Location:", "Address:", "City:", "Based in:" (must be at start of line or after newline)
            r'(?:^|\n)\s*(?:location|address|city|based\s+in|residing\s+in|current\s+location)[:\s]+([A-Z][a-zA-Z\s,]+(?:,\s*[A-Z]{2})?)(?:\s+[0-9]{5})?(?:\n|$)',
            # Pattern: City, State (e.g., "New York, NY", "San Francisco, CA") - must be standalone
            r'\b([A-Z][a-zA-Z\s]{2,20}),\s*([A-Z]{2})\b(?!\s*(?:testing|deployment|development|product))',
            # Pattern: City, Country (e.g., "London, UK", "Toronto, Canada")
            r'\b([A-Z][a-zA-Z\s]{2,20}),\s*([A-Z][a-zA-Z\s]{2,20})\b(?!\s*(?:testing|deployment|development|product))',
        ]
        
        # Common major cities and locations to look for
        common_locations = [
            'New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Boston',
            'Seattle', 'Austin', 'Denver', 'Miami', 'Atlanta', 'Dallas',
            'London', 'Toronto', 'Sydney', 'Melbourne', 'Berlin', 'Paris',
            'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai',
            'Kathmandu', 'Kathmandu Valley', 'Nepal', 'India', 'USA', 'United States'
        ]
        
        # Try structured patterns first
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                location = match.group(0).strip()
                # Clean up common prefixes
                location = re.sub(r'^(?:location|address|city|based\s+in|residing\s+in|current\s+location)[:\s]+', '', location, flags=re.IGNORECASE)
                location = re.sub(r'^(?:lives?\s+in|located\s+in|from)\s+', '', location, flags=re.IGNORECASE)
                location = location.strip()
                
                # Validate: check if it contains invalid keywords (likely not a location)
                location_lower = location.lower()
                if any(keyword in location_lower for keyword in invalid_keywords):
                    continue
                
                # Validate length and format
                if 3 <= len(location) <= 50 and ',' in location:  # Prefer "City, State" format
                    return location
                elif 3 <= len(location) <= 30:  # Single city name
                    return location
        
        # Try to find common city names with better context validation
        for city in common_locations:
            # Look for city name with context (not just in the middle of another word)
            pattern = rf'\b{re.escape(city)}\b'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Get context around the match
                context_start = max(0, match.start() - 100)
                context_end = min(len(text), match.end() + 100)
                context = text[context_start:context_end].lower()
                
                # Check if context suggests this is NOT a location
                if any(keyword in context for keyword in invalid_keywords):
                    # Check if invalid keyword is closer to the city name than location indicators
                    city_pos = match.start() - context_start
                    invalid_positions = [context.find(kw) for kw in invalid_keywords if kw in context]
                    location_indicators = ['location', 'address', 'city', 'based', 'residing', 'from', 'lives']
                    location_positions = [context.find(li) for li in location_indicators if li in context]
                    
                    # If invalid keyword is closer than location indicators, skip
                    if invalid_positions and (not location_positions or min([abs(p - city_pos) for p in invalid_positions if p >= 0]) < min([abs(p - city_pos) for p in location_positions if p >= 0])):
                        continue
                
                # Try to get city, state/country if available
                state_match = re.search(rf'{re.escape(city)},\s*([A-Z][A-Za-z\s]+)', text[context_start:context_end], re.IGNORECASE)
                if state_match:
                    full_location = state_match.group(0).strip()
                    if len(full_location) <= 50:
                        return full_location
                else:
                    # Return just the city if it's a known location
                    return city
        
        return None

