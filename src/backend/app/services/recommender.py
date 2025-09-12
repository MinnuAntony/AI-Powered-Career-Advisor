from app.utils.preprocessing import normalize_grades, analyze_strengths
from app.schemas import CareerRequest, CareerResponse, CareerRecommendation, AlternativePathway
from typing import List, Dict

# --- Existing mappings ---
CAREER_MAP = {
    "math": ["Data Scientist", "Actuary", "AI Engineer"],
    "physics": ["Robotics Engineer", "AI Engineer", "Astronomer"],
    "computer_science": ["Software Engineer", "AI Engineer", "Data Scientist"],
    "biology": ["Biomedical Researcher", "Doctor", "Biotech Specialist"],
    "chemistry": ["Chemist", "Pharmacist", "Biochemist"],
    "english": ["Writer", "Content Strategist", "Editor"],
    "history": ["Historian", "Museum Curator", "Archaeologist"]
}

INTEREST_KEYWORDS = {
    "ai": ["Data Scientist", "AI Engineer"],
    "coding": ["Software Engineer", "Data Scientist"],
    "robotics": ["Robotics Engineer"],
    "biology": ["Biomedical Researcher", "Doctor"],
    "writing": ["Writer", "Content Strategist"]
}

def prioritize_by_interests(careers: List[str], interests_text: str) -> List[str]:
    interests_lower = interests_text.lower()
    prioritized = set(careers)
    for keyword, keyword_careers in INTEREST_KEYWORDS.items():
        if keyword in interests_lower:
            prioritized.update(keyword_careers)
    return list(prioritized)

# --- Placeholder for LangChain + Bedrock ---
def ai_based_recommendations(processed_data: Dict) -> str:
    """
    This is a placeholder function. Later, it will:
    - Embed processed_data with Titan embeddings
    - Query ChromaDB vector store
    - Pass results + context to Claude LLM (Bedrock)
    """
    return "AI reasoning will appear here once dataset and Bedrock integration are complete."

# --- Combined pipeline ---
def generate_recommendations(request: CareerRequest) -> CareerResponse:
    # Step 1: Normalize and analyze
    normalized = normalize_grades(request.grades)
    strengths = analyze_strengths(normalized)

    # Step 2: Rule-based career selection
    careers = []
    for subject, level in strengths.items():
        if level == "Strong" and subject.lower() in CAREER_MAP:
            careers.extend(CAREER_MAP[subject.lower()])
    careers = prioritize_by_interests(careers, request.interests)
    careers = list(dict.fromkeys(careers))[:5]

    recommendations = []
    for career in careers:
        recommendations.append(
            CareerRecommendation(
                career=career,
                reasoning=f"Based on strong performance in {', '.join([s for s, lvl in strengths.items() if lvl == 'Strong'])} and interests in '{request.interests}'.",
                avg_salary="N/A",
                growth="N/A",
                roadmap=[]
            )
        )

    # Step 3: Placeholder AI output
    ai_output = ai_based_recommendations({
        "grades": normalized,
        "strengths": strengths,
        "interests": request.interests
    })

    # Step 4: Placeholder alternative pathways
    alternative_pathways = [
        AlternativePathway(
            field="AI Ethics",
            note="Emerging field combining logic and CS."
        )
    ]

    return CareerResponse(
        recommendations=recommendations,
        alternative_pathways=alternative_pathways
    )
