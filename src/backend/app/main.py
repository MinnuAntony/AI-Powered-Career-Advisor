from fastapi import FastAPI
from app.routes import recommend, jobs, assess
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = FastAPI(
    title="AI-Powered Career Advisor",
    description="Backend for career recommendations, job insights, and assessments",
    version="0.2.0"
)

# Register routes
app.include_router(recommend.router, prefix="/api/v1", tags=["Career Advisor"])
app.include_router(jobs.router, prefix="/api/v1", tags=["Job Market"])
app.include_router(assess.router, prefix="/api/v1", tags=["Assessment"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
