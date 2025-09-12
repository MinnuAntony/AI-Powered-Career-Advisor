from fastapi import FastAPI
from app.routes import recommend

app = FastAPI(
    title="AI-Powered Career Advisor",
    description="Backend for career recommendations using grades + interests",
    version="0.1.0"
)

# Register routes
app.include_router(recommend.router, prefix="/api/v1", tags=["Career Advisor"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
