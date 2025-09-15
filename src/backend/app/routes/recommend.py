from fastapi import APIRouter
from app.schemas.career import CareerRequest, CareerResponse
from app.services.recommender import generate_recommendations

router = APIRouter()

@router.post("/recommend", response_model=CareerResponse)
def recommend_career(request: CareerRequest):
    """
    Endpoint to generate career recommendations.
    Uses AI reasoning + job market insights.
    """
    return generate_recommendations(request)
    