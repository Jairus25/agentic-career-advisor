"""
FastAPI REST API for Agentic AI Career Advisor
Run with: uvicorn api_server:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from main import AgenticCareerAdvisor, StudentProfile as BaseStudentProfile

app = FastAPI(
    title="Agentic AI Career Advisor API",
    description="Multi-agent AI system for personalized career guidance",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class StudentProfileRequest(BaseModel):
    name: str
    education_level: str
    major: str
    skills: List[str]
    interests: List[str]
    career_goals: str
    experience: List[str]

class SkillsAnalysisResponse(BaseModel):
    analysis: str

class CareerMatchesResponse(BaseModel):
    matches: str

class LearningPathRequest(BaseModel):
    profile: StudentProfileRequest
    target_career: str

class LearningPathResponse(BaseModel):
    learning_path: str

class IndustryResearchResponse(BaseModel):
    research: str

class ComprehensiveAdviceResponse(BaseModel):
    skills_analysis: str
    career_matches: str
    action_plan: str

# Initialize advisor
try:
    advisor = AgenticCareerAdvisor()
except ValueError as e:
    print("Warning: ANTHROPIC_API_KEY not found. API will not function properly.")
    advisor = None

def convert_to_base_profile(profile: StudentProfileRequest) -> BaseStudentProfile:
    """Convert API request model to base StudentProfile"""
    return BaseStudentProfile(
        name=profile.name,
        education_level=profile.education_level,
        major=profile.major,
        skills=profile.skills,
        interests=profile.interests,
        career_goals=profile.career_goals,
        experience=profile.experience
    )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Agentic AI Career Advisor API",
        "version": "1.0.0",
        "endpoints": {
            "skills_analysis": "/analyze/skills",
            "career_matches": "/match/careers",
            "learning_path": "/create/learning-path",
            "industry_research": "/research/industry/{industry_name}",
            "comprehensive_advice": "/advice/comprehensive"
        },
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "advisor_initialized": advisor is not None
    }

@app.post("/analyze/skills", response_model=SkillsAnalysisResponse)
async def analyze_skills(profile: StudentProfileRequest):
    """
    Analyze student's skills and provide development recommendations
    """
    if not advisor:
        raise HTTPException(status_code=500, detail="Advisor not initialized")
    
    try:
        base_profile = convert_to_base_profile(profile)
        analysis = advisor.analyze_skills(base_profile)
        return SkillsAnalysisResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match/careers", response_model=CareerMatchesResponse)
async def match_careers(profile: StudentProfileRequest):
    """
    Find career paths that match the student's profile
    """
    if not advisor:
        raise HTTPException(status_code=500, detail="Advisor not initialized")
    
    try:
        base_profile = convert_to_base_profile(profile)
        matches = advisor.find_career_matches(base_profile)
        return CareerMatchesResponse(matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create/learning-path", response_model=LearningPathResponse)
async def create_learning_path(request: LearningPathRequest):
    """
    Generate a personalized learning roadmap for target career
    """
    if not advisor:
        raise HTTPException(status_code=500, detail="Advisor not initialized")
    
    try:
        base_profile = convert_to_base_profile(request.profile)
        path = advisor.create_learning_path(base_profile, request.target_career)
        return LearningPathResponse(learning_path=path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/industry/{industry_name}", response_model=IndustryResearchResponse)
async def research_industry(industry_name: str):
    """
    Get current trends and insights about an industry
    """
    if not advisor:
        raise HTTPException(status_code=500, detail="Advisor not initialized")
    
    try:
        research = advisor.research_industry(industry_name)
        return IndustryResearchResponse(research=research)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/advice/comprehensive", response_model=ComprehensiveAdviceResponse)
async def comprehensive_advice(profile: StudentProfileRequest):
    """
    Get comprehensive career advice from all agents
    """
    if not advisor:
        raise HTTPException(status_code=500, detail="Advisor not initialized")
    
    try:
        base_profile = convert_to_base_profile(profile)
        advice = advisor.get_comprehensive_advice(base_profile)
        return ComprehensiveAdviceResponse(
            skills_analysis=advice["skills_analysis"],
            career_matches=advice["career_matches"],
            action_plan=advice["action_plan"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
