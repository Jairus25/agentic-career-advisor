"""
Agentic AI Career Advisor for Students
A multi-agent system for personalized career guidance
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

# Install required packages:
# pip install anthropic python-dotenv

import anthropic
from dotenv import load_dotenv

load_dotenv()

class AgentRole(Enum):
    COORDINATOR = "coordinator"
    SKILLS_ANALYZER = "skills_analyzer"
    CAREER_MATCHER = "career_matcher"
    LEARNING_PATHFINDER = "learning_pathfinder"
    INDUSTRY_RESEARCHER = "industry_researcher"

@dataclass
class StudentProfile:
    name: str
    education_level: str
    major: str
    skills: List[str]
    interests: List[str]
    career_goals: str
    experience: List[str]

class CareerAdvisorAgent:
    """Base class for all career advisor agents"""
    
    def __init__(self, role: AgentRole, api_key: str):
        self.role = role
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def get_system_prompt(self) -> str:
        prompts = {
            AgentRole.COORDINATOR: """You are a Career Advisor Coordinator. Your role is to:
1. Understand student queries and profiles
2. Delegate tasks to specialized agents
3. Synthesize responses from all agents into coherent career advice
4. Ensure all aspects of career planning are covered""",
            
            AgentRole.SKILLS_ANALYZER: """You are a Skills Analysis Agent. Your role is to:
1. Analyze student's current skills and experiences
2. Identify skill gaps for desired careers
3. Assess transferable skills
4. Provide skill development recommendations""",
            
            AgentRole.CAREER_MATCHER: """You are a Career Matching Agent. Your role is to:
1. Match student profiles with suitable career paths
2. Consider interests, skills, and market demand
3. Provide career options with growth potential
4. Explain why each career is a good fit""",
            
            AgentRole.LEARNING_PATHFINDER: """You are a Learning Path Agent. Your role is to:
1. Design personalized learning roadmaps
2. Recommend courses, certifications, and resources
3. Create timeline-based learning plans
4. Suggest practical projects and experiences""",
            
            AgentRole.INDUSTRY_RESEARCHER: """You are an Industry Research Agent. Your role is to:
1. Provide current industry trends and insights
2. Analyze job market conditions
3. Share salary expectations and growth projections
4. Identify emerging opportunities in various sectors"""
        }
        return prompts[self.role]
    
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        messages = [{"role": "user", "content": query}]
        
        if context:
            context_str = f"Context: {context}\n\n{query}"
            messages = [{"role": "user", "content": context_str}]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.get_system_prompt(),
            messages=messages
        )
        
        return response.content[0].text

class AgenticCareerAdvisor:
    """Main orchestrator for the multi-agent career advisor system"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        
        self.agents = {
            role: CareerAdvisorAgent(role, self.api_key)
            for role in AgentRole
        }
        
    def create_student_context(self, profile: StudentProfile) -> str:
        return f"""
Student Profile:
- Name: {profile.name}
- Education: {profile.education_level} in {profile.major}
- Skills: {', '.join(profile.skills)}
- Interests: {', '.join(profile.interests)}
- Career Goals: {profile.career_goals}
- Experience: {', '.join(profile.experience)}
"""
    
    def analyze_skills(self, profile: StudentProfile) -> str:
        context = self.create_student_context(profile)
        query = "Analyze this student's skills and provide recommendations for skill development."
        return self.agents[AgentRole.SKILLS_ANALYZER].process(query, {"profile": context})
    
    def find_career_matches(self, profile: StudentProfile) -> str:
        context = self.create_student_context(profile)
        query = "Based on this student's profile, suggest 3-5 career paths that would be good matches."
        return self.agents[AgentRole.CAREER_MATCHER].process(query, {"profile": context})
    
    def create_learning_path(self, profile: StudentProfile, target_career: str) -> str:
        context = self.create_student_context(profile)
        query = f"Create a detailed learning path for this student to pursue a career in {target_career}."
        return self.agents[AgentRole.LEARNING_PATHFINDER].process(query, {"profile": context})
    
    def research_industry(self, industry: str) -> str:
        query = f"Provide current trends, job market insights, and opportunities in the {industry} industry."
        return self.agents[AgentRole.INDUSTRY_RESEARCHER].process(query)
    
    def get_comprehensive_advice(self, profile: StudentProfile) -> Dict[str, str]:
        """Get comprehensive career advice from all agents"""
        
        # Gather insights from all specialized agents
        skills_analysis = self.analyze_skills(profile)
        career_matches = self.find_career_matches(profile)
        
        # Coordinate and synthesize
        coordinator_query = f"""
Based on the following analyses, provide comprehensive career advice:

SKILLS ANALYSIS:
{skills_analysis}

CAREER MATCHES:
{career_matches}

Student Profile:
{self.create_student_context(profile)}

Provide a cohesive career action plan.
"""
        
        final_advice = self.agents[AgentRole.COORDINATOR].process(coordinator_query)
        
        return {
            "skills_analysis": skills_analysis,
            "career_matches": career_matches,
            "action_plan": final_advice
        }

# Example usage
def main():
    # Create a sample student profile
    student = StudentProfile(
        name="Alex Johnson",
        education_level="Bachelor's (3rd year)",
        major="Computer Science",
        skills=["Python", "JavaScript", "Data Structures", "Web Development"],
        interests=["AI/ML", "Problem Solving", "Building Products"],
        career_goals="Work in AI/ML or become a software engineer at a tech company",
        experience=["Internship at local startup", "Personal coding projects", "University coding club"]
    )
    
    # Initialize the career advisor system
    advisor = AgenticCareerAdvisor()
    
    print("🎓 Agentic AI Career Advisor\n")
    print("=" * 60)
    
    # Get comprehensive advice
    advice = advisor.get_comprehensive_advice(student)
    
    print("\n📊 SKILLS ANALYSIS")
    print("-" * 60)
    print(advice["skills_analysis"])
    
    print("\n\n💼 CAREER MATCHES")
    print("-" * 60)
    print(advice["career_matches"])
    
    print("\n\n🎯 ACTION PLAN")
    print("-" * 60)
    print(advice["action_plan"])
    
    # Get specific learning path
    print("\n\n📚 LEARNING PATH FOR ML ENGINEER")
    print("-" * 60)
    learning_path = advisor.create_learning_path(student, "Machine Learning Engineer")
    print(learning_path)
    
    # Research an industry
    print("\n\n🔍 INDUSTRY RESEARCH: AI/ML")
    print("-" * 60)
    industry_insights = advisor.research_industry("Artificial Intelligence and Machine Learning")
    print(industry_insights)

if __name__ == "__main__":
    main()
