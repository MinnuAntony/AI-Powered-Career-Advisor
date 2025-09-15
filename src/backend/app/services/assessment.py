from app.schemas.assess import AssessmentRequest, AssessmentResponse

# Define domains and question scoring
QUIZ_DOMAINS = {
    "Analytical": [
        "I enjoy solving puzzles and logical problems.",
        "I like working with numbers and patterns.",
        "I enjoy analyzing data to make decisions."
    ],
    "Creative": [
        "I enjoy drawing, designing, or writing creatively.",
        "I like thinking of unique solutions to problems.",
        "I enjoy brainstorming and imagining new ideas."
    ],
    "Leadership": [
        "I enjoy leading group activities or projects.",
        "I like making decisions for a team.",
        "I motivate and guide others effectively."
    ],
    "Communication": [
        "I enjoy explaining ideas clearly to others.",
        "I like writing or presenting my thoughts.",
        "I can persuade or influence others easily."
    ]
}

def evaluate_assessment(request: AssessmentRequest) -> AssessmentResponse:
    """
    Score a personality quiz and return multi-trait assessment.
    Each answer is expected as a numeric value: 0, 1, 2.
    """
    answers = request.answers  # e.g., {"Analytical": [2,1,2], "Creative": [1,2,1], ...}

    trait_scores = {}
    for domain, scores in answers.items():
        trait_scores[domain] = sum(scores)

    # Determine primary and secondary traits
    sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
    primary_trait = sorted_traits[0][0]
    secondary_trait = sorted_traits[1][0] if len(sorted_traits) > 1 else None

    # Suggest careers based on top traits (can be customized later)
    trait_to_career_map = {
        "Analytical": ["Data Scientist", "Financial Analyst"],
        "Creative": ["Designer", "Content Creator"],
        "Leadership": ["Project Manager", "Entrepreneur"],
        "Communication": ["Technical Writer", "Marketing Specialist"]
    }
    suggested_careers = trait_to_career_map.get(primary_trait, [])

    return AssessmentResponse(
        personality_traits=trait_scores,
        primary_trait=primary_trait,
        secondary_trait=secondary_trait,
        suggested_careers=suggested_careers
    )
