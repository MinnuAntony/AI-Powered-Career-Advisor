
# app/services/job_market.py
from app.schemas.job import JobMarketResponse, JobMarketInsight
from langchain_aws import ChatBedrock
from app.utils.parsers import extract_json_from_text

def get_job_market_data(career: str) -> JobMarketResponse:
    """
    Fetch job market insights using Bedrock AI.
    Falls back to mock data if AI fails.
    """
    try:
        llm = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")

        prompt = f"""
        Provide a JSON-formatted object containing job market info for the career "{career}".
        Include:
        - demand: current market demand (High/Medium/Low)
        - avg_salary: average salary range in USD
        - future_outlook: expected growth in next 5-10 years
        Format as JSON only.
        """

        response = llm.invoke(prompt)
        text = response.content[0].text if isinstance(response.content, list) else response.content

        data = extract_json_from_text(text)
        demand = data.get("demand", "Unknown")
        avg_salary = data.get("avg_salary", "N/A")
        future_outlook = data.get("future_outlook", "Unknown")

    except Exception as e:
        print(f"Bedrock AI failed: {e}")
        # Fallback mock data
        demand = "High"
        avg_salary = "$70,000 - $120,000"
        future_outlook = "Growing"

    insight = JobMarketInsight(
        career=career,
        demand=demand,
        avg_salary=avg_salary,
        future_outlook=future_outlook
    )

    return JobMarketResponse(insights=insight)
