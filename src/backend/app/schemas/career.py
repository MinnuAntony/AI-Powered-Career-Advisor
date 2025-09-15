from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from app.schemas.assess import AssessmentResponse  # import the assessment schema

class CareerRequest(BaseModel):
    grades: Dict[str, float] = Field(..., example={"math": 85, "english": 75})
    interests: str = Field(..., example="I enjoy coding and robotics.")
    assessment: Optional[AssessmentResponse] = None  # <-- new field

class CareerRecommendation(BaseModel):
    career: str
    reasoning: str
    avg_salary: Optional[str] = None
    growth: Optional[str] = None
    roadmap: List[str] = []

class AlternativePathway(BaseModel):
    field: str
    note: str

class CareerResponse(BaseModel):
    recommendations: List[CareerRecommendation]
    alternative_pathways: Optional[List[AlternativePathway]] = []
