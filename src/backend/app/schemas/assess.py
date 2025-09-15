from pydantic import BaseModel
from typing import Dict, List, Optional

class AssessmentRequest(BaseModel):
    """
    Quiz answers submitted by the student.
    Each domain contains a list of numeric scores per question.
    Example: {"Analytical": [2,1,2], "Creative": [1,2,1]}
    """
    answers: Dict[str, List[int]]

class AssessmentResponse(BaseModel):
    """
    Output of the assessment.
    - personality_traits: all domain scores
    - primary_trait: highest scoring trait
    - secondary_trait: second highest (optional)
    - suggested_careers: careers mapped from top trait
    """
    personality_traits: Dict[str, int]
    primary_trait: str
    secondary_trait: Optional[str] = None
    suggested_careers: List[str]
