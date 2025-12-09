"""
Google Gemini AI Service for intelligent chatbot responses
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional

class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.model = None
        self.is_available = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Try different models in order of preference (including latest naming)
                models_to_try = [
                    'models/gemini-1.5-flash',
                    'models/gemini-pro', 
                    'models/gemini-1.0-pro',
                    'gemini-1.5-flash-latest',
                    'gemini-pro-latest',
                    'gemini-1.5-pro',
                ]
                for model_name in models_to_try:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        # Test the model with a simple request
                        test_response = self.model.generate_content("Hi")
                        self.is_available = True
                        print(f"✅ Gemini AI initialized successfully with model: {model_name}")
                        break
                    except Exception as model_error:
                        print(f"⚠️ Model {model_name} not available: {model_error}")
                        continue
                
                if not self.is_available:
                    print("⚠️ No Gemini models available. Using fallback responses.")
            except Exception as e:
                print(f"⚠️ Gemini AI initialization failed: {e}")
                self.is_available = False
        else:
            print("⚠️ GEMINI_API_KEY not set. AI chatbot will use fallback responses.")
    
    def get_career_response(self, 
                           user_message: str, 
                           user_context: Dict,
                           conversation_history: List[Dict] = None) -> Dict:
        """
        Generate an intelligent career guidance response using Gemini AI
        
        Args:
            user_message: The user's message/question
            user_context: User profile data (skills, experience, target role, etc.)
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dict with 'message', 'suggestions', and 'data' fields
        """
        if not self.is_available:
            return self._fallback_response(user_message, user_context)
        
        try:
            # Build the system context
            system_prompt = self._build_system_prompt(user_context)
            
            # Build the conversation
            full_prompt = f"""{system_prompt}

User's Question: {user_message}

Please provide a helpful, personalized career guidance response. Be specific, actionable, and encouraging.
If the user asks about jobs, skills, or career paths, use their profile information to give personalized advice.
Keep responses concise but informative (2-4 paragraphs max).
End with 2-3 specific follow-up suggestions the user might want to explore.

Response format:
1. Main response (helpful, personalized advice)
2. Suggestions: [list 2-3 follow-up actions or questions]
"""
            
            # Generate response
            print(f"🤖 Calling Gemini AI for: {user_message[:50]}...")
            response = self.model.generate_content(full_prompt)
            
            # Parse the response
            response_text = response.text
            print(f"✅ Gemini AI responded successfully")
            
            # Extract suggestions if present
            suggestions = self._extract_suggestions(response_text)
            main_message = self._clean_response(response_text)
            
            return {
                'message': main_message,
                'suggestions': suggestions,
                'ai_powered': True
            }
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_response(user_message, user_context)
    
    def _build_system_prompt(self, user_context: Dict) -> str:
        """Build a context-aware system prompt"""
        
        skills = user_context.get('skills', [])
        if isinstance(skills, list):
            skills_str = ', '.join(skills) if skills else 'Not specified'
        else:
            skills_str = str(skills) if skills else 'Not specified'
            
        return f"""You are an expert AI Career Counselor and Mentor. You help users navigate their career paths with personalized, actionable advice.

USER PROFILE:
- Name: {user_context.get('name', 'User')}
- Current Skills: {skills_str}
- Experience: {user_context.get('experience_years', 0)} years
- Current Role: {user_context.get('current_role', 'Not specified')}
- Target Role: {user_context.get('target_role', 'Not specified')}
- Location: {user_context.get('location', 'Not specified')}
- Education: {user_context.get('education', 'Not specified')}

YOUR GUIDELINES:
1. Be warm, encouraging, and professional
2. Give specific, actionable advice based on their profile
3. Reference their actual skills and experience when relevant
4. Suggest concrete next steps they can take
5. If they're missing skills for their target role, be supportive and provide a learning path
6. Use bullet points for clarity when listing steps or skills
7. Be honest but constructive about skill gaps
8. Consider current job market trends in your advice"""
    
    def _extract_suggestions(self, response_text: str) -> List[str]:
        """Extract follow-up suggestions from the response"""
        suggestions = []
        
        # Look for suggestions section
        if 'Suggestions:' in response_text:
            parts = response_text.split('Suggestions:')
            if len(parts) > 1:
                suggestion_text = parts[1].strip()
                # Parse bullet points or numbered items
                lines = suggestion_text.split('\n')
                for line in lines:
                    line = line.strip()
                    # Remove common bullet/number prefixes
                    for prefix in ['- ', '• ', '* ', '1. ', '2. ', '3. ', '4. ', '5. ']:
                        if line.startswith(prefix):
                            line = line[len(prefix):]
                            break
                    if line and len(line) > 5:
                        suggestions.append(line)
                        if len(suggestions) >= 3:
                            break
        
        # Default suggestions if none found
        if not suggestions:
            suggestions = [
                "Tell me more about my skill gaps",
                "Show me job opportunities",
                "Create a learning plan for me"
            ]
        
        return suggestions[:3]
    
    def _clean_response(self, response_text: str) -> str:
        """Clean up the response text"""
        # Remove the suggestions section if present
        if 'Suggestions:' in response_text:
            response_text = response_text.split('Suggestions:')[0]
        
        return response_text.strip()
    
    def _fallback_response(self, user_message: str, user_context: Dict) -> Dict:
        """Provide intelligent fallback responses based on user context"""
        message_lower = user_message.lower()
        
        name = user_context.get('name', 'there')
        target_role = user_context.get('target_role', '')
        current_role = user_context.get('current_role', '')
        skills = user_context.get('skills', [])
        experience_years = user_context.get('experience_years', 0)
        location = user_context.get('location', '')
        
        # Process skills list
        if isinstance(skills, list):
            skills_list = [s if isinstance(s, str) else s.get('name', '') for s in skills]
            skills_str = ', '.join(skills_list[:8]) if skills_list else 'Not specified'
        else:
            skills_list = []
            skills_str = 'Not specified'
        
        # Career role recommendations based on skills
        skill_to_roles = {
            'python': ['Data Scientist', 'ML Engineer', 'Backend Developer', 'DevOps Engineer'],
            'javascript': ['Frontend Developer', 'Full Stack Developer', 'React Developer'],
            'react': ['Frontend Developer', 'Full Stack Developer', 'UI Developer'],
            'java': ['Backend Developer', 'Software Engineer', 'Android Developer'],
            'sql': ['Data Analyst', 'Database Administrator', 'Backend Developer'],
            'machine learning': ['ML Engineer', 'Data Scientist', 'AI Engineer'],
            'aws': ['Cloud Engineer', 'DevOps Engineer', 'Solutions Architect'],
            'docker': ['DevOps Engineer', 'Platform Engineer', 'Backend Developer'],
            'node': ['Backend Developer', 'Full Stack Developer'],
            'mongodb': ['Backend Developer', 'Full Stack Developer', 'Database Developer'],
            'html': ['Frontend Developer', 'Web Developer', 'UI Developer'],
            'css': ['Frontend Developer', 'Web Developer', 'UI/UX Developer'],
        }
        
        # Find recommended roles based on user's skills
        recommended_roles = set()
        for skill in skills_list:
            skill_lower = skill.lower()
            for key, roles in skill_to_roles.items():
                if key in skill_lower:
                    recommended_roles.update(roles)
        recommended_roles = list(recommended_roles)[:5]
        
        # Skills needed for common roles
        role_skills = {
            'data scientist': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'TensorFlow'],
            'ml engineer': ['Python', 'TensorFlow', 'PyTorch', 'MLOps', 'Docker', 'AWS'],
            'full stack developer': ['JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB', 'Git'],
            'frontend developer': ['JavaScript', 'React', 'HTML', 'CSS', 'TypeScript', 'Git'],
            'backend developer': ['Python', 'Java', 'SQL', 'REST APIs', 'Docker', 'Git'],
            'devops engineer': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Linux', 'Terraform'],
            'software engineer': ['Programming', 'Data Structures', 'Algorithms', 'Git', 'SQL'],
        }
        
        # Greeting
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
            message = f"Hello {name}! 👋 Welcome to your AI Career Counselor!\n\n"
            if skills_list:
                message += f"I see you have skills in: **{skills_str}**\n\n"
            if target_role:
                message += f"Your target role is: **{target_role}**\n\n"
            message += "I can help you with:\n• 📊 Career path planning\n• 💼 Finding matching jobs\n• 📈 Skill gap analysis\n• 📚 Learning recommendations\n\nWhat would you like to explore?"
            suggestions = ["Analyze my skills", "Find jobs for me", "Show my career path"]
        
        # Career recommendations
        elif any(word in message_lower for word in ['career', 'recommend', 'suggestion', 'advice', 'guidance']):
            if skills_list and recommended_roles:
                message = f"Based on your skills ({skills_str}), here are career paths that suit you:\n\n"
                for i, role in enumerate(recommended_roles[:4], 1):
                    message += f"**{i}. {role}**\n"
                message += f"\n💡 With {experience_years} years of experience, you're well-positioned for mid-level roles."
                if target_role:
                    message += f"\n\nYour current target is **{target_role}** - great choice! Would you like me to analyze your skill gaps for this role?"
            else:
                message = f"I'd love to help you find the perfect career path, {name}!\n\nTo give you personalized recommendations, I need to know your skills. Please:\n1. Upload your resume, or\n2. Update your profile with your skills\n\nThen I can suggest roles that match your background!"
            suggestions = ["Show skill gaps", "Update my profile", "Explore all roles"]
        
        # Job search
        elif any(word in message_lower for word in ['job', 'jobs', 'work', 'opportunity', 'hiring', 'position']):
            if target_role:
                message = f"🔍 **Job Search for {target_role}**\n\n"
                if skills_list:
                    message += f"Based on your skills ({', '.join(skills_list[:5])}), I'm finding jobs that match your profile.\n\n"
                if location:
                    message += f"📍 Searching in: {location}\n\n"
                message += "Check the **Dashboard** for personalized job recommendations with direct links to apply!\n\n"
                message += "💡 **Tip:** Keep your skills updated to get better job matches."
            else:
                message = "I can help you find job opportunities! 💼\n\nTo get the best job recommendations:\n1. Set your **target role** in your Profile\n2. Make sure your **skills** are up to date\n3. Check the **Dashboard** for personalized matches\n\nWhat type of role are you looking for?"
            suggestions = ["Go to Dashboard", "Update target role", "Show remote jobs"]
        
        # Skill analysis
        elif any(word in message_lower for word in ['skill', 'skills', 'analyze', 'gap', 'missing', 'need', 'learn']):
            if target_role and target_role.lower() in role_skills:
                required = role_skills[target_role.lower()]
                user_skills_lower = [s.lower() for s in skills_list]
                missing = [s for s in required if s.lower() not in ' '.join(user_skills_lower)]
                matching = [s for s in required if s.lower() in ' '.join(user_skills_lower)]
                
                match_pct = len(matching) / len(required) * 100 if required else 0
                
                message = f"📊 **Skill Analysis for {target_role}**\n\n"
                message += f"**Match Score:** {match_pct:.0f}%\n\n"
                
                if matching:
                    message += f"✅ **Skills you have:** {', '.join(matching)}\n\n"
                if missing:
                    message += f"📚 **Skills to learn:** {', '.join(missing)}\n\n"
                    message += f"💡 **Recommendation:** Focus on learning **{missing[0]}** first - it's essential for this role!"
                else:
                    message += "🎉 Great news! You have all the core skills for this role. Consider applying for jobs!"
            elif skills_list:
                message = f"📊 **Your Skill Profile**\n\n"
                message += f"**Current Skills:** {skills_str}\n\n"
                if recommended_roles:
                    message += f"**Roles that match your skills:**\n"
                    for role in recommended_roles[:3]:
                        message += f"• {role}\n"
                message += f"\n💡 Set a **target role** in your Profile to see specific skill gaps!"
            else:
                message = "I'd love to analyze your skills! 📊\n\nTo get started:\n1. **Upload your resume** - I'll extract your skills automatically\n2. Or **update your profile** with your skills manually\n\nThen I can show you skill gaps for any career role!"
            suggestions = ["Show learning resources", "Update my skills", "View career path"]
        
        # Learning resources
        elif any(word in message_lower for word in ['learn', 'course', 'tutorial', 'resource', 'study', 'training']):
            message = f"📚 **Learning Resources**\n\n"
            if target_role:
                message += f"For your goal of becoming a **{target_role}**, I recommend:\n\n"
                if target_role.lower() in role_skills:
                    skills_to_learn = role_skills[target_role.lower()][:3]
                    for skill in skills_to_learn:
                        message += f"• **{skill}** - Search YouTube or Coursera for tutorials\n"
            else:
                message += "Popular skills to learn in 2024:\n\n"
                message += "• **Python** - Most versatile programming language\n"
                message += "• **React** - Top frontend framework\n"
                message += "• **AWS** - Leading cloud platform\n"
                message += "• **SQL** - Essential for data roles\n"
            message += "\n🎯 Check the **Roadmap** page for structured learning paths!"
            suggestions = ["Go to Roadmap", "Show skill gaps", "Find jobs"]
        
        # Default response
        else:
            message = f"Hi {name}! 👋 I'm your Career Guidance Assistant.\n\n"
            if skills_list:
                message += f"**Your Profile:**\n"
                message += f"• Skills: {skills_str}\n"
                if target_role:
                    message += f"• Target Role: {target_role}\n"
                if experience_years:
                    message += f"• Experience: {experience_years} years\n"
                message += "\n"
            message += "**How can I help you today?**\n\n"
            message += "• 💼 \"Find jobs\" - Get job recommendations\n"
            message += "• 📊 \"Analyze skills\" - See your skill gaps\n"
            message += "• 🎯 \"Career advice\" - Get personalized guidance\n"
            message += "• 📚 \"Learning resources\" - Find courses & tutorials"
            suggestions = ["Analyze my skills", "Find jobs", "Get career advice"]
        
        return {
            'message': message,
            'suggestions': suggestions,
            'ai_powered': False
        }
    
    def analyze_resume_with_ai(self, resume_text: str) -> Dict:
        """Use Gemini to analyze a resume and extract insights"""
        if not self.is_available:
            return None
            
        try:
            prompt = f"""Analyze this resume and extract the following information in JSON format:
            
Resume:
{resume_text[:5000]}  # Limit to first 5000 chars

Extract:
1. skills: List of technical and soft skills
2. experience_years: Estimated years of experience (number)
3. current_role: Their current or most recent job title
4. education: Highest education level
5. strengths: 3 key strengths
6. areas_to_improve: 3 areas they could improve
7. recommended_roles: 3 career roles that would suit them

Return as JSON only, no additional text."""

            response = self.model.generate_content(prompt)
            
            # Try to parse as JSON
            import json
            try:
                # Clean up the response to get just JSON
                text = response.text.strip()
                if text.startswith('```json'):
                    text = text[7:]
                if text.startswith('```'):
                    text = text[3:]
                if text.endswith('```'):
                    text = text[:-3]
                    
                return json.loads(text)
            except json.JSONDecodeError:
                return None
                
        except Exception as e:
            print(f"Resume analysis error: {e}")
            return None


# Global instance
gemini_service = GeminiService()

