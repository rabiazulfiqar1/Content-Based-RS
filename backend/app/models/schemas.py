from pydantic import BaseModel
from typing import List, Optional

# ============================================
# USER PROFILE SCHEMAS
# ============================================

class UserSkillCreate(BaseModel):
    skill_id: int
    proficiency: int  # 1-5

class UserProfileCreate(BaseModel):
    skill_level: str  # 'beginner', 'intermediate', 'advanced'
    interests: List[str]
    bio: Optional[str] = None
    github_username: Optional[str] = None
    preferred_project_types: Optional[List[str]] = None
    skills: List[UserSkillCreate]

class BasicProfileCreate(BaseModel):
    full_name: str  # Required now
    username: str   # Required now
    organization: Optional[str] = None
    field_of_study: Optional[str] = None
    phone: Optional[str] = None
    profile_pic: Optional[str] = None

# ============================================
# PROJECT SCHEMAS
# ============================================

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    repo_url: Optional[str]
    difficulty: str
    topics: List[str]
    estimated_hours: int
    source: str
    stars: int
    language: str

class RecommendationResponse(BaseModel):
    project_id: int
    title: str
    description: str
    repo_url: Optional[str]
    difficulty: str
    topics: List[str]
    estimated_hours: int
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    reason: str
    semantic_similarity: Optional[float] = None  
    source: str  # NEW: 'github', 'kaggle_competition', 'kaggle_dataset', 'curated'

# ============================================
# INTERACTION SCHEMAS
# ============================================

class InteractionCreate(BaseModel):
    project_id: int
    interaction_type: str  # 'viewed', 'bookmarked', 'started', 'completed'
    rating: Optional[int] = None  # 1-5
    
class UserActivitySummary(BaseModel):
    total_interactions: int
    projects_viewed: int
    projects_bookmarked: int
    projects_started: int
    projects_completed: int
    avg_rating: Optional[float]
    total_learning_hours: int
    skills_count: int
    most_active_category: Optional[str]
    recent_activity_7d: int
    completion_rate: float
