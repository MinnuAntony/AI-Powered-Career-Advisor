from typing import Dict, List

from app.utils.preprocessing import normalize_grades, analyze_strengths
from app.utils.parsers import extract_json_from_text
from app.schemas.career import (
    CareerRequest,
    CareerResponse,
    CareerRecommendation,
    AlternativePathway
)
from app.services.job_market import get_job_market_data
from app.prompts.career_prompts import career_prompt

# LangChain + Bedrock
from langchain_aws import ChatBedrock


def ai_based_recommendations(processed_data: Dict, assessment: Dict) -> List[Dict]:
    """
    AI reasoning with Claude 3.5 Sonnet via Bedrock.
    Uses LangChain PromptTemplate for flexibility.
    """
    try:
        llm = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")

        # Build prompt dynamically
        prompt = career_prompt.format(
            grades=processed_data['grades'],
            strengths=processed_data['strengths'],
            interests=processed_data['interests'],
            assessment=assessment or "No assessment data provided"
        )

        response = llm.invoke(prompt)
        print(response)
        text = response.content[0].text if isinstance(response.content, list) else response.content

        # Use the utility parser to extract JSON
        ai_json = extract_json_from_text(text)
        return ai_json

    except Exception as e:
        return [{
            "career": "AI module error",
            "reasoning": str(e),
            "avg_salary": "N/A",
            "growth": "N/A",
            "roadmap": []
        }]


def generate_recommendations(request: CareerRequest) -> CareerResponse:
    """
    Generate career recommendations by combining:
    - Student-centric analysis
    - AI reasoning (Claude)
    - Job market insights
    """
    # Step 1: Normalize grades and analyze strengths
    normalized = normalize_grades(request.grades)
    strengths = analyze_strengths(normalized)

    # Step 2: Prepare assessment data (if any)
    assessment_data = request.assessment.dict() if request.assessment else None

    # Step 3: Get AI-based career recommendations
    ai_results = ai_based_recommendations(
        {
            "grades": normalized,
            "strengths": strengths,
            "interests": request.interests
        },
        assessment=assessment_data
    )

    recommendations = []
    for item in ai_results:
        career_name = item.get("career", "Unknown")

        # Step 4: Enrich with job market insights
        job_data = get_job_market_data(career_name)

        recommendations.append(
            CareerRecommendation(
                career=career_name,
                reasoning=item.get("reasoning", ""),
                avg_salary=item.get("avg_salary", ""),
                # avg_salary=job_data.insights.avg_salary if job_data else "N/A",
                growth=job_data.insights.future_outlook if job_data else item.get("growth", "N/A"),
                roadmap=item.get("roadmap", [])
            )
        )

    # Step 5: Placeholder alternative pathways
    alternative_pathways = [
        AlternativePathway(
            field="AI Ethics",
            note="Emerging field combining logic and computer science."
        )
    ]

    return CareerResponse(
        recommendations=recommendations[:7],
        alternative_pathways=alternative_pathways
    )
