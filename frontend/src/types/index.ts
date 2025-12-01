// Type definitions for the application

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  skills?: any[];
  experience_years?: number;
  current_role?: string;
  target_role?: string;
}

export interface Recommendation {
  roles: Role[];
  jobs: Job[];
  resources: LearningResource[];
}

export interface Role {
  id: number;
  title: string;
  description: string;
  required_skills: string[];
  score?: number;
}

export interface Job {
  id: number;
  title: string;
  company: string;
  description: string;
  required_skills: string[];
  location?: string;
  score?: number;
}

export interface LearningResource {
  id: number;
  title: string;
  description: string;
  resource_type: string;
  url?: string;
  skills_covered: string[];
  duration?: string;
}
