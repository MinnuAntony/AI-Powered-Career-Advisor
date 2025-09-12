from fastapi import APIRouter
from app.schemas import CareerRequest, CareerResponse, CareerRecommendation, AlternativePathway
from app.services.recommender import generate_recommendations

router = APIRouter()

@router.post("/recommend", response_model=CareerResponse)
def recommend_career(request: CareerRequest):
    return generate_recommendations(request)
