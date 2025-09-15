from fastapi import APIRouter
from app.schemas.job import JobMarketResponse
from app.services.job_market import get_job_market_data

router = APIRouter()

@router.get("/jobs", response_model=JobMarketResponse)
def job_market_insights(career: str):
    """
    Endpoint to fetch job market insights for a given career.
    """
    return get_job_market_data(career)
