from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  #  Import
from app.routes import recommend, jobs, assess
from app.services import chatbot  # 👈 new
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = FastAPI(
    title="AI-Powered Career Advisor",
    description="Backend for career recommendations, job insights, and assessments",
    version="0.2.0"
)

#  Add CORS middleware
origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "https://your-frontend-domain.com",  # when deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],         # allow GET, POST, PUT, DELETE etc.
    allow_headers=["*"],
)

# Register routes
app.include_router(recommend.router, prefix="/api/v1", tags=["Career Advisor"])
app.include_router(jobs.router, prefix="/api/v1", tags=["Job Market"])
app.include_router(assess.router, prefix="/api/v1", tags=["Assessment"])
app.include_router(chatbot.router, prefix="/api/v1", tags=["Chatbot"])  # 👈 new


@app.get("/health")
def health_check():
    return {"status": "ok"}
