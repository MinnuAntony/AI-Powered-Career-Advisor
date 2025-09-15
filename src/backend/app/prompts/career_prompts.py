from langchain.prompts import PromptTemplate

career_prompt = PromptTemplate(
    input_variables=["grades", "strengths", "interests", "assessment"],
    template="""
You are an AI career advisor.
Student profile:
Grades: {grades}
Strengths: {strengths}
Interests: {interests}
Assessment: {assessment}

Based on this, recommend 3–5 realistic career options.
Important:
- Consider job market demand in the student's country.
- Align recommendations with personality traits and strengths.
- If interests lack career scope, explain limitations and suggest alternatives.
- Include growth outlook based on market trends.

For each career, include:
- career name
- reasoning
- avg_salary
- growth
- roadmap (3–5 bullet steps)

Return the result as valid JSON list of objects with keys:
career, reasoning, avg_salary, growth, roadmap
"""
)
