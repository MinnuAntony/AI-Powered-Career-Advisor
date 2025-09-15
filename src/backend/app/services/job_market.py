from app.schemas.job import JobMarketResponse, JobMarketInsight

def get_job_market_data(career: str) -> JobMarketResponse:
    """
    Placeholder for real job market APIs (LinkedIn, Glassdoor, etc.)
    Right now returns mock data.
    """
    return JobMarketResponse(
        insights=JobMarketInsight(
            career=career,
            demand="High",
            avg_salary="$70,000 - $120,000",
            future_outlook="Growing"
        )
    )
