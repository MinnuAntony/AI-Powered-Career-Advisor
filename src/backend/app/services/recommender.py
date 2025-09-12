from app.utils.preprocessing import normalize_grades, analyze_strengths
from app.schemas import CareerRequest, CareerResponse, CareerRecommendation, AlternativePathway
from typing import List

# Step 1: Define a simple career mapping
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
    """
    Boost careers if keywords appear in interests.
    """
    interests_lower = interests_text.lower()
    prioritized = set(careers)

    for keyword, keyword_careers in INTEREST_KEYWORDS.items():
        if keyword in interests_lower:
            prioritized.update(keyword_careers)

    return list(prioritized)

def generate_recommendations(request: CareerRequest) -> CareerResponse:
    # Step 1: Normalize grades and analyze strengths
    normalized = normalize_grades(request.grades)
    strengths = analyze_strengths(normalized)

    # Step 2: Gather careers based on strong subjects
    careers = []
    for subject, level in strengths.items():
        if level == "Strong" and subject.lower() in CAREER_MAP:
            careers.extend(CAREER_MAP[subject.lower()])
    
    # Step 3: Prioritize careers based on interests
    careers = prioritize_by_interests(careers, request.interests)

    # Remove duplicates and limit top 5
    careers = list(dict.fromkeys(careers))[:5]

    # Step 4: Build CareerRecommendation objects
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

    # Step 5: Add placeholder alternative pathways
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
