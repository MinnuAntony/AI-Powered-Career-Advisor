from fastapi import APIRouter
from app.schemas.assess import AssessmentRequest, AssessmentResponse
from app.services.assessment import evaluate_assessment

router = APIRouter()

@router.post("/assess", response_model=AssessmentResponse)
def assess_student(request: AssessmentRequest):
    """
    Submit quiz answers to get personality assessment.
    """
    return evaluate_assessment(request)
