from fastapi import APIRouter
from app.schemas import CareerRequest, CareerResponse
from app.services.recommender import generate_recommendations

router = APIRouter()

@router.post("/recommend", response_model=CareerResponse)
def recommend_career(request: CareerRequest):
    """
    Endpoint to generate career recommendations.
    Currently uses rule-based logic with a placeholder for AI reasoning.
    """
    return generate_recommendations(request)
