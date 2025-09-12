from app.utils.preprocessing import normalize_grades, analyze_strengths
from app.schemas import CareerRequest, CareerResponse, CareerRecommendation, AlternativePathway
from typing import List, Dict
import json
import re

# LangChain + Bedrock
from langchain_aws import ChatBedrock

# --- Existing mappings (rule-based fallback) ---
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


def ai_based_recommendations(processed_data: Dict) -> str:
    """
    Direct AI reasoning with Claude 3.5 Sonnet via Bedrock.
    No dataset, just prompt-based guidance.
    """
    try:
        llm = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")


        prompt = f"""
        You are an AI career advisor.
        Student profile:
        Grades: {processed_data['grades']}
        Strengths: {processed_data['strengths']}
        Interests: {processed_data['interests']}

        Based on this, recommend 3-5 career options.
        For each career, include:
        - career name
        - reasoning (why it fits)
        - avg_salary (rough estimate, global or US)
        - growth (market outlook)
        - roadmap (3-5 bullet steps student should take)

        Return the result as valid JSON list of objects with keys:
        career, reasoning, avg_salary, growth, roadmap
        """

        response = llm.invoke(prompt)
        print(response)   # Debug: see what Bedrock actually returns


        text = response.content[0].text if isinstance(response.content, list) else response.content

        # Step 2: extract JSON inside code fences (```json ... ```) if present
        match = re.search(r"```json\s*(\[.*\])\s*```", text, re.DOTALL)
        if match:
            clean_json = match.group(1)
        else:
            clean_json = text.strip()  # fallback: maybe raw JSON

        # Step 3: parse JSON
        ai_json = json.loads(clean_json)
        return ai_json


    except Exception as e:
        return [{"career": "AI module error", "reasoning": str(e), "avg_salary": "N/A", "growth": "N/A", "roadmap": []}]


def generate_recommendations(request: CareerRequest) -> CareerResponse:
    # Step 1: Normalize and analyze
    normalized = normalize_grades(request.grades)
    strengths = analyze_strengths(normalized)

    # Step 2: Rule-based career selection (fallback)
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

    # Step 3: AI recommendations (Claude, no dataset)
    ai_results = ai_based_recommendations({
        "grades": normalized,
        "strengths": strengths,
        "interests": request.interests
    })

    if isinstance(ai_results, list):
        for item in ai_results:
            recommendations.append(
                CareerRecommendation(
                    career=item.get("career", "Unknown"),
                    reasoning=item.get("reasoning", ""),
                    avg_salary=item.get("avg_salary", "N/A"),
                    growth=item.get("growth", "N/A"),
                    roadmap=item.get("roadmap", [])
                )
            )

    # Step 4: Placeholder alternative pathways
    alternative_pathways = [
        AlternativePathway(
            field="AI Ethics",
            note="Emerging field combining logic and CS."
        )
    ]

    return CareerResponse(
        recommendations=recommendations[:7],
        alternative_pathways=alternative_pathways
    )
