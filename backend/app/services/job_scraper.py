"""
Job scraping service - Scrape real-time job postings from LinkedIn and other sources
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from datetime import datetime
import time
import urllib.parse

class JobScraper:
    """Scrape job postings from LinkedIn and other sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.linkedin_base = 'https://www.linkedin.com/jobs/search'
    
    def scrape_linkedin_jobs(self, job_title: str, location: str = "", skills: List[str] = None, limit: int = 10) -> List[Dict]:
        """Scrape jobs from LinkedIn with proper links, location filtering, and skill-based search"""
        jobs = []
        
        try:
            # Build LinkedIn search URL with job title and skills
            # Combine job title with top skills for better matching
            search_terms = [job_title]
            if skills and len(skills) > 0:
                # Add top 2-3 most relevant skills to search query
                top_skills = skills[:3]
                search_terms.extend(top_skills)
            
            keywords = urllib.parse.quote(' '.join(search_terms))
            
            # Always include location if provided
            if location and location.strip():
                location_param = urllib.parse.quote(location.strip())
                url = f"{self.linkedin_base}?keywords={keywords}&location={location_param}&start=0"
            else:
                url = f"{self.linkedin_base}?keywords={keywords}&start=0"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings - LinkedIn uses various class names
                job_cards = soup.find_all('div', class_=re.compile(r'job-search-card|base-card|job-card-container'))
                
                # Also try finding by data attributes
                if not job_cards:
                    job_cards = soup.find_all('li', class_=re.compile(r'jobs-search-results__list-item'))
                
                for card in job_cards[:limit]:
                    try:
                        # Try multiple selectors for job title
                        title_elem = (
                            card.find('h3', class_=re.compile(r'base-search-card__title|job-result-card__title')) or
                            card.find('a', class_=re.compile(r'base-card__full-link|job-card-list__title')) or
                            card.find('span', {'aria-label': re.compile(r'.*', re.IGNORECASE)})
                        )
                        
                        # Try multiple selectors for company
                        company_elem = (
                            card.find('h4', class_=re.compile(r'base-search-card__subtitle|job-result-card__subtitle')) or
                            card.find('a', class_=re.compile(r'job-result-card__subtitle-link')) or
                            card.find('span', class_=re.compile(r'job-result-card__subtitle'))
                        )
                        
                        # Try multiple selectors for location
                        location_elem = (
                            card.find('span', class_=re.compile(r'job-search-card__location|job-result-card__location')) or
                            card.find('span', {'aria-label': re.compile(r'Location', re.IGNORECASE)})
                        )
                        
                        # Get job link
                        link_elem = card.find('a', href=re.compile(r'/jobs/view/|/jobs/search/'))
                        job_link = None
                        if link_elem:
                            href = link_elem.get('href', '')
                            if href.startswith('/'):
                                job_link = f"https://www.linkedin.com{href}"
                            elif href.startswith('http'):
                                job_link = href
                        
                        # If no direct link found, construct from job ID
                        if not job_link:
                            # Try to extract job ID from data attributes
                            job_id = card.get('data-job-id') or card.get('data-entity-urn', '').split(':')[-1]
                            if job_id:
                                job_link = f"https://www.linkedin.com/jobs/view/{job_id}"
                        
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True) if company_elem else 'Company not specified'
                            
                            # Get and validate location
                            location_text = None
                            if location_elem:
                                location_text = location_elem.get_text(strip=True)
                                # Validate location - should not contain job description keywords
                                invalid_location_keywords = ['testing', 'deployment', 'development', 'product', 'ui', 'ux', 'api', 'server']
                                if any(keyword in location_text.lower() for keyword in invalid_location_keywords):
                                    location_text = None  # Invalid location, ignore it
                            
                            # Use fallback location only if it's valid
                            if not location_text:
                                if location and location.strip() and len(location.strip()) < 50:
                                    # Validate fallback location too
                                    invalid_keywords = ['testing', 'deployment', 'development', 'product', 'ui', 'ux']
                                    if not any(keyword in location.lower() for keyword in invalid_keywords):
                                        location_text = location.strip()
                            
                            if not location_text:
                                location_text = 'Location not specified'
                            
                            # Get description if available
                            desc_elem = card.find('p', class_=re.compile(r'job-search-card__snippet|job-result-card__snippet'))
                            description = desc_elem.get_text(strip=True) if desc_elem else ''
                            
                            job = {
                                'title': title,
                                'company': company,
                                'location': location_text,
                                'description': description[:200] + '...' if len(description) > 200 else description,
                                'url': job_link or f"{self.linkedin_base}?keywords={keywords}",
                                'source': 'linkedin',
                                'scraped_at': datetime.now().isoformat()
                            }
                            jobs.append(job)
                    except Exception as e:
                        print(f"Error parsing LinkedIn job card: {e}")
                        continue
            else:
                print(f"LinkedIn returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
            # Return empty list, will fall back to generated jobs
        
        return jobs
    
    def scrape_glassdoor(self, job_title: str, location: str = "", limit: int = 10) -> List[Dict]:
        """Scrape jobs from Glassdoor (example - be careful with rate limiting)"""
        jobs = []
        
        try:
            # Glassdoor requires more complex handling
            # This is a simplified example
            query = f"{job_title} {location}".strip()
            url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query.replace(' ', '+')}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Parse Glassdoor structure (may need adjustment)
                # Implementation similar to Indeed
                pass
        except Exception as e:
            print(f"Error scraping Glassdoor: {e}")
        
        return jobs
    
    def scrape_generic_job_boards(self, job_title: str, skills: List[str] = None, location: str = "") -> List[Dict]:
        """Generate realistic job postings based on job title, skills, and location (fallback when scraping fails)"""
        jobs = []
        
        # Common companies for tech jobs
        companies = [
            'Tech Corp', 'Innovation Labs', 'Digital Solutions Inc', 'Cloud Services Ltd',
            'Data Analytics Co', 'Software Innovations', 'AI Technologies', 'Web Solutions',
            'DevOps Experts', 'Full Stack Solutions', 'Code Masters', 'Tech Startups Inc'
        ]
        
        # Generate diverse job titles based on skills and base role
        job_titles = self._generate_diverse_job_titles(job_title, skills or [])
        
        # Use user location if provided, otherwise use common locations
        if location and location.strip() and len(location.strip()) < 50:  # Validate location length
            # Use user's location for generated jobs
            job_locations = [location.strip()] * len(job_titles)
            # Add a few nearby/remote options
            job_locations.extend(['Remote', f"Near {location.strip()}"])
        else:
            # Default locations if no user location or invalid location
            job_locations = [
                'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
                'Remote', 'Boston, MA', 'Chicago, IL', 'Denver, CO'
            ]
        
        # Generate job postings with diverse titles based on skills
        for i, title in enumerate(job_titles[:10]):
            # Select relevant skills for this specific job title (not all skills)
            relevant_skills = self._select_relevant_skills_for_job(title, skills or [])
            
            # Build LinkedIn search URL with this specific title and selected skills
            search_terms = [title]
            if relevant_skills:
                search_terms.extend([str(s) for s in relevant_skills[:2]])  # Add top 2 relevant skills
            
            keywords = urllib.parse.quote(' '.join(search_terms))
            if location and location.strip() and len(location.strip()) < 50:
                location_param = urllib.parse.quote(location.strip())
                linkedin_search_url = f"{self.linkedin_base}?keywords={keywords}&location={location_param}"
            else:
                linkedin_search_url = f"{self.linkedin_base}?keywords={keywords}"
            
            job = {
                'title': title,
                'company': companies[i % len(companies)],
                'location': job_locations[i % len(job_locations)] if i < len(job_locations) else 'Remote',
                'description': self._generate_job_description(title, skills or []),
                'required_skills': relevant_skills,  # Only relevant skills, not all skills
                'url': linkedin_search_url,
                'source': 'generated',
                'scraped_at': datetime.now().isoformat()
            }
            jobs.append(job)
        
        return jobs
    
    def _generate_diverse_job_titles(self, base_role: str, skills: List[str]) -> List[str]:
        """Generate diverse job titles based on skills and base role"""
        titles = []
        base_lower = base_role.lower()
        
        # Skill-based title variations
        skill_to_role = {
            'react': 'React Developer',
            'angular': 'Angular Developer',
            'vue': 'Vue.js Developer',
            'node': 'Node.js Developer',
            'python': 'Python Developer',
            'java': 'Java Developer',
            'javascript': 'JavaScript Developer',
            'typescript': 'TypeScript Developer',
            'django': 'Django Developer',
            'flask': 'Flask Developer',
            'spring': 'Spring Boot Developer',
            'mongodb': 'MongoDB Developer',
            'postgresql': 'PostgreSQL Developer',
            'mysql': 'MySQL Developer',
            'docker': 'DevOps Engineer',
            'kubernetes': 'Kubernetes Engineer',
            'aws': 'AWS Engineer',
            'machine learning': 'Machine Learning Engineer',
            'data science': 'Data Scientist',
            'tensorflow': 'ML Engineer',
            'pytorch': 'Deep Learning Engineer'
        }
        
        # Level variations
        levels = ['Junior', 'Mid-Level', 'Senior', 'Lead', '']
        
        # Generate titles based on skills
        skill_titles = []
        for skill in skills[:5]:  # Use top 5 skills
            skill_lower = str(skill).lower().strip()
            for key, role in skill_to_role.items():
                if key in skill_lower:
                    skill_titles.append(role)
                    break
        
        # Create diverse titles
        if skill_titles:
            # Use skill-based titles
            for skill_title in skill_titles[:3]:
                for level in ['', 'Senior', 'Mid-Level']:
                    if level:
                        titles.append(f"{level} {skill_title}")
                    else:
                        titles.append(skill_title)
        
        # Add full-stack variations if relevant skills present
        fullstack_skills = ['react', 'angular', 'vue', 'node', 'javascript', 'typescript', 'python', 'java']
        has_frontend = any(skill in str(s).lower() for s in skills for skill in ['react', 'angular', 'vue', 'javascript'])
        has_backend = any(skill in str(s).lower() for s in skills for skill in ['node', 'python', 'java', 'django', 'flask', 'spring'])
        
        if has_frontend and has_backend:
            titles.extend([
                'Full Stack Developer',
                'Full Stack Engineer',
                'Senior Full Stack Developer',
                'Full Stack Web Developer'
            ])
        elif has_frontend:
            titles.extend([
                'Frontend Developer',
                'Front-End Engineer',
                'UI Developer',
                'React Developer'
            ])
        elif has_backend:
            titles.extend([
                'Backend Developer',
                'Back-End Engineer',
                'Server-Side Developer',
                'API Developer'
            ])
        
        # Add base role variations
        if base_role:
            titles.append(base_role)
            titles.append(f"Senior {base_role}")
            titles.append(f"{base_role} (Remote)")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_titles = []
        for title in titles:
            title_lower = title.lower()
            if title_lower not in seen:
                seen.add(title_lower)
                unique_titles.append(title)
        
        # Ensure we have at least 5 titles
        while len(unique_titles) < 5:
            unique_titles.append(f"{base_role} - {len(unique_titles) + 1}")
        
        return unique_titles[:10]  # Return up to 10 diverse titles
    
    def _generate_job_description(self, job_title: str, skills: List[str]) -> str:
        """Generate a realistic job description with subset of skills"""
        # Use only a subset of skills (2-4 skills) to make it more realistic
        if skills and len(skills) > 0:
            # Select 2-4 relevant skills based on job title
            selected_skills = self._select_relevant_skills_for_job(job_title, skills)
            skills_text = ', '.join(selected_skills[:4])
        else:
            skills_text = 'relevant technologies'
            selected_skills = []
        
        base_description = f"""
        We are looking for a {job_title} to join our team. 
        The ideal candidate will have experience with {skills_text}.
        
        Responsibilities:
        - Design and develop scalable solutions
        - Collaborate with cross-functional teams
        - Write clean, maintainable code
        - Participate in code reviews
        
        Requirements:
        - Strong experience in {', '.join(selected_skills[:2]) if selected_skills else 'programming'}
        - Excellent problem-solving skills
        - Good communication skills
        """
        return base_description.strip()
    
    def _select_relevant_skills_for_job(self, job_title: str, all_skills: List[str]) -> List[str]:
        """Select relevant skills for a specific job title"""
        job_title_lower = job_title.lower()
        selected = []
        remaining = all_skills.copy()
        
        # Priority mapping: skills that are highly relevant to specific job types
        priority_map = {
            'react': ['react', 'javascript', 'js', 'typescript', 'html', 'css'],
            'frontend': ['react', 'javascript', 'html', 'css', 'angular', 'vue'],
            'backend': ['python', 'java', 'node', 'django', 'flask', 'spring'],
            'full stack': ['react', 'node', 'javascript', 'python', 'mongodb', 'sql'],
            'python': ['python', 'django', 'flask', 'sql', 'postgresql'],
            'java': ['java', 'spring', 'sql', 'mysql', 'mongodb'],
            'node': ['node', 'javascript', 'react', 'mongodb', 'express'],
        }
        
        # Find relevant skills based on job title
        for key, relevant_skills in priority_map.items():
            if key in job_title_lower:
                # Select skills that match the job type
                for skill in all_skills:
                    skill_lower = str(skill).lower()
                    if any(rel_skill in skill_lower for rel_skill in relevant_skills):
                        if skill not in selected:
                            selected.append(skill)
                            if skill in remaining:
                                remaining.remove(skill)
                break
        
        # If no specific match, select 2-4 diverse skills
        if len(selected) < 2:
            # Select a mix of different skill types
            selected = all_skills[:min(4, len(all_skills))]
        else:
            # Add 1-2 additional skills for variety
            if remaining:
                selected.extend(remaining[:2])
        
        return selected[:4]  # Return max 4 skills
    
    def get_linkedin_search_url(self, job_title: str, location: str = "") -> str:
        """Generate LinkedIn job search URL for a given role"""
        keywords = urllib.parse.quote(job_title)
        if location:
            location_param = urllib.parse.quote(location)
            return f"{self.linkedin_base}?keywords={keywords}&location={location_param}"
        return f"{self.linkedin_base}?keywords={keywords}"
    
    def get_linkedin_profile_search_url(self, full_name: str = "", location: str = "", current_role: str = "") -> str:
        """Generate LinkedIn profile search URL based on resume data"""
        # LinkedIn people search URL
        linkedin_people_base = 'https://www.linkedin.com/search/results/people/'
        
        params = []
        
        # Add name if available
        if full_name:
            # Extract first and last name if possible
            name_parts = full_name.strip().split()
            if len(name_parts) >= 2:
                params.append(f"firstName={urllib.parse.quote(name_parts[0])}")
                params.append(f"lastName={urllib.parse.quote(' '.join(name_parts[1:]))}")
            else:
                params.append(f"keywords={urllib.parse.quote(full_name)}")
        
        # Add location if available
        if location:
            # Extract city from location (e.g., "New York, NY" -> "New York")
            location_parts = location.split(',')
            city = location_parts[0].strip()
            params.append(f"geoUrn=%5B%22{urllib.parse.quote(city)}%22%5D")
        
        # Add current role/title if available
        if current_role:
            params.append(f"title={urllib.parse.quote(current_role)}")
        
        if params:
            return f"{linkedin_people_base}?{'&'.join(params)}"
        
        # Fallback to general LinkedIn search
        search_terms = []
        if full_name:
            search_terms.append(full_name)
        if location:
            search_terms.append(location)
        if current_role:
            search_terms.append(current_role)
        
        if search_terms:
            query = urllib.parse.quote(' '.join(search_terms))
            return f"{linkedin_people_base}?keywords={query}"
        
        return "https://www.linkedin.com/"
    
    def get_jobs_for_user(self, user_skills: List[str], target_role: str, location: str = "") -> List[Dict]:
        """Get jobs matching user profile from LinkedIn and other sources, filtered by location and personalized by skills"""
        all_jobs = []
        
        # Normalize skills (handle both string and dict formats)
        normalized_skills = []
        for skill in (user_skills or []):
            if isinstance(skill, str):
                normalized_skills.append(skill.lower().strip())
            elif isinstance(skill, dict):
                normalized_skills.append(skill.get('name', '').lower().strip())
        
        # Remove empty skills
        normalized_skills = [s for s in normalized_skills if s]
        
        # Try scraping LinkedIn with skill-specific searches (with error handling)
        try:
            # Search 1: Role + top skills
            if location and location.strip():
                linkedin_jobs = self.scrape_linkedin_jobs(target_role, location.strip(), normalized_skills, limit=20)
                print(f"Scraping LinkedIn jobs for '{target_role}' with skills {normalized_skills[:3]} in location '{location}'")
            else:
                linkedin_jobs = self.scrape_linkedin_jobs(target_role, "", normalized_skills, limit=20)
                print(f"Scraping LinkedIn jobs for '{target_role}' with skills {normalized_skills[:3]} (no location specified)")
            
            # Search 2: If we have multiple skills, try searching with different skill combinations
            if len(normalized_skills) > 3:
                try:
                    # Try a second search with different skill combinations for diversity
                    additional_skills = normalized_skills[3:6] if len(normalized_skills) > 6 else normalized_skills[1:4]
                    if location and location.strip():
                        additional_jobs = self.scrape_linkedin_jobs(target_role, location.strip(), additional_skills, limit=10)
                    else:
                        additional_jobs = self.scrape_linkedin_jobs(target_role, "", additional_skills, limit=10)
                    
                    # Merge additional jobs, avoiding duplicates
                    existing_titles = {(j.get('title', ''), j.get('company', '')) for j in linkedin_jobs}
                    for job in additional_jobs:
                        job_key = (job.get('title', ''), job.get('company', ''))
                        if job_key not in existing_titles:
                            linkedin_jobs.append(job)
                except Exception as e:
                    print(f"Additional skill-based search failed: {e}")
            
            if linkedin_jobs:
                # Filter jobs by location if location is provided
                if location and location.strip():
                    location_lower = location.strip().lower()
                    # Filter jobs that match location (case-insensitive partial match)
                    location_filtered = []
                    for job in linkedin_jobs:
                        job_location = job.get('location', '').lower()
                        # Check if location matches (city, state, or contains location keywords)
                        if (location_lower in job_location or 
                            any(part in job_location for part in location_lower.split(',')) or
                            any(part in job_location for part in location_lower.split())):
                            location_filtered.append(job)
                    
                    # If we found location-matched jobs, use them; otherwise use all scraped jobs
                    if location_filtered:
                        all_jobs.extend(location_filtered)
                        print(f"Found {len(location_filtered)} jobs matching location '{location}'")
                    else:
                        all_jobs.extend(linkedin_jobs)
                        print(f"Using all {len(linkedin_jobs)} scraped jobs (location filtering found none)")
                else:
                    all_jobs.extend(linkedin_jobs)
                    print(f"Successfully scraped {len(linkedin_jobs)} jobs from LinkedIn")
        except Exception as e:
            print(f"LinkedIn scraping failed: {e}")
        
        # If we got LinkedIn jobs, use them. Otherwise generate fallback jobs with location
        if not all_jobs:
            # Generate additional jobs based on skills and location as fallback
            generated_jobs = self.scrape_generic_job_boards(target_role, user_skills, location)
            all_jobs.extend(generated_jobs)
        
        # Score and rank jobs based on skill match (personalized scoring)
        for job in all_jobs:
            job['match_score'] = self._calculate_match_score(job, normalized_skills)
            # Add skill match details for transparency
            job['matched_skills'] = self._get_matched_skills(job, normalized_skills)
            # Ensure all jobs have a URL with skills
            if 'url' not in job or not job['url']:
                search_terms = [target_role] + normalized_skills[:3]
                keywords = urllib.parse.quote(' '.join(search_terms))
                if location:
                    location_param = urllib.parse.quote(location)
                    job['url'] = f"{self.linkedin_base}?keywords={keywords}&location={location_param}"
                else:
                    job['url'] = f"{self.linkedin_base}?keywords={keywords}"
        
        # Filter out jobs with very low skill match (less than 10% match)
        # This ensures only relevant jobs are shown
        filtered_jobs = [job for job in all_jobs if job.get('match_score', 0) >= 0.10]
        
        # If we filtered out too many, keep at least top 5 even with lower scores (but >= 5%)
        if len(filtered_jobs) < 5:
            # Sort all jobs and take top 5
            all_jobs.sort(key=lambda x: (
                0 if x.get('source') == 'linkedin' else 1,  # LinkedIn jobs first
                -x.get('match_score', 0.01)  # Then by match score descending
            ))
            filtered_jobs = [j for j in all_jobs if j.get('match_score', 0) >= 0.05][:5]
        
        # Sort filtered jobs by match score (LinkedIn jobs first, then by score)
        filtered_jobs.sort(key=lambda x: (
            0 if x.get('source') == 'linkedin' else 1,  # LinkedIn jobs first
            -x.get('match_score', 0.10)  # Then by match score descending
        ))
        
        # Ensure diversity: if we have multiple jobs with same title, keep only the best one
        seen_titles = {}
        diverse_jobs = []
        for job in filtered_jobs:
            title_lower = job.get('title', '').lower()
            if title_lower not in seen_titles:
                seen_titles[title_lower] = job
                diverse_jobs.append(job)
            else:
                # If this job has a better match score, replace the previous one
                if job.get('match_score', 0) > seen_titles[title_lower].get('match_score', 0):
                    # Remove old one and add new one
                    diverse_jobs = [j for j in diverse_jobs if j.get('title', '').lower() != title_lower]
                    diverse_jobs.append(job)
                    seen_titles[title_lower] = job
        
        # Re-sort after deduplication
        diverse_jobs.sort(key=lambda x: (
            0 if x.get('source') == 'linkedin' else 1,  # LinkedIn jobs first
            -x.get('match_score', 0.10)  # Then by match score descending
        ))
        
        return diverse_jobs[:10]  # Return top 10 diverse, personalized jobs
    
    def _calculate_match_score(self, job: Dict, user_skills: List[str]) -> float:
        """Calculate how well job matches user skills (realistic personalized scoring)"""
        if not user_skills:
            # If no skills provided, give a base score
            return 0.1  # 10% base match
        
        # Normalize user skills
        normalized_user_skills = [str(s).lower().strip() for s in user_skills if s]
        
        # Combine all job text for skill matching
        job_text = (
            job.get('title', '') + ' ' + 
            job.get('description', '') + ' ' + 
            job.get('company', '')
        ).lower()
        
        job_skills = job.get('required_skills', [])
        job_skills_normalized = [str(js).lower().strip() for js in job_skills if js]
        
        # Also extract skills from description if not in required_skills
        if not job_skills_normalized:
            # Try to extract skills from description
            description = job.get('description', '').lower()
            for skill in normalized_user_skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', description):
                    job_skills_normalized.append(skill)
        
        # Count exact skill matches (higher weight)
        exact_matches = 0
        partial_matches = 0
        matched_skill_list = []
        
        for skill in normalized_user_skills:
            if not skill:
                continue
                
            # Check for exact match in job skills list
            if any(skill == js for js in job_skills_normalized):
                exact_matches += 1
                matched_skill_list.append(skill)
            # Check for exact match in job text (word boundary)
            elif re.search(r'\b' + re.escape(skill) + r'\b', job_text):
                exact_matches += 1
                matched_skill_list.append(skill)
            # Check for partial match (skill appears anywhere in text) - lower weight
            elif skill in job_text:
                partial_matches += 1
        
        # Calculate score based on job requirements vs user skills
        # Score = (matched skills / job required skills) * (matched skills / user total skills)
        # This prevents 100% match when job has fewer requirements than user has skills
        
        num_job_skills = len(job_skills_normalized) if job_skills_normalized else max(1, exact_matches + partial_matches)
        num_user_skills = len(normalized_user_skills)
        
        # Calculate weighted score
        # Exact matches are worth 2x, partial matches are worth 0.5x
        total_weighted_matches = (exact_matches * 2.0) + (partial_matches * 0.5)
        
        # Calculate match ratio: how many of job's required skills does user have?
        job_match_ratio = min(1.0, total_weighted_matches / (num_job_skills * 2.0)) if num_job_skills > 0 else 0.0
        
        # Calculate coverage ratio: how many of user's skills are used in this job?
        user_coverage_ratio = min(1.0, (exact_matches + partial_matches) / num_user_skills) if num_user_skills > 0 else 0.0
        
        # Combined score: balance between job requirements match and user skill utilization
        # Job match ratio is more important (70%), user coverage is less (30%)
        score = (job_match_ratio * 0.7) + (user_coverage_ratio * 0.3)
        
        # Boost score if job title matches user's target role or key skills
        job_title_lower = job.get('title', '').lower()
        title_match_boost = 0.0
        for skill in normalized_user_skills[:5]:  # Check top 5 skills
            if skill in job_title_lower:
                title_match_boost += 0.1  # 10% boost per matching skill in title
        
        score = min(1.0, score + title_match_boost)
        
        # Ensure score is realistic - cap at 95% unless truly exceptional match
        if score > 0.95 and (exact_matches < num_user_skills * 0.8):
            score = 0.95
        
        return max(0.05, min(0.95, score))  # Return score between 5% and 95%
    
    def _get_matched_skills(self, job: Dict, user_skills: List[str]) -> List[str]:
        """Get list of user skills that match the job"""
        if not user_skills:
            return []
        
        matched = []
        normalized_user_skills = [str(s).lower().strip() for s in user_skills if s]
        
        job_text = (
            job.get('title', '') + ' ' + 
            job.get('description', '') + ' ' + 
            ' '.join(job.get('required_skills', []))
        ).lower()
        
        for skill in normalized_user_skills:
            if not skill:
                continue
            # Check if skill appears in job (exact or partial match)
            if re.search(r'\b' + re.escape(skill) + r'\b', job_text) or skill in job_text:
                # Return original case skill if possible
                original_skill = next((s for s in user_skills if str(s).lower().strip() == skill), skill)
                if original_skill not in matched:
                    matched.append(original_skill if isinstance(original_skill, str) else str(original_skill))
        
        return matched[:5]  # Return top 5 matched skills

