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

def ai_based_recommendations(processed_data: Dict) -> str:
    """
    Skeleton for AI integration (Bedrock + LangChain).

    Steps to implement later:
    1. Embed student interests + strengths using Titan embeddings.
    2. Query ChromaDB vector store (career dataset embeddings).
    3. Pass retrieved careers + student info to Claude 3.5 Sonnet.
    4. Generate structured recommendations: career, roadmap, market outlook.
    """
    try:
        # Example pseudo-code for future integration
        # from langchain.embeddings import BedrockEmbeddings
        # from langchain.vectorstores import Chroma
        # from langchain.chains import RetrievalQA
        # from langchain.chat_models import BedrockChat

        # embeddings = BedrockEmbeddings(model_id="amazon.titan-text-v2")
        # llm = BedrockChat(model_id="anthropic.claude-3.5-sonnet")
        # vector_store = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
        # retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":5})
        # qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        # query = f"Student data: {processed_data}"
        # ai_output = qa_chain.run(query)
        ai_output = "AI reasoning will appear here once dataset is integrated."
    except Exception as e:
        ai_output = f"AI module not ready: {str(e)}"
    return ai_output
    
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
