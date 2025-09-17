import os
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock

# Load AWS creds
load_dotenv()

router = APIRouter()

# -------------------------
# LangGraph State
# -------------------------
class QAState(dict):
    question: str
    answer: str

# -------------------------
# Nodes
# -------------------------
def validate_question(state: QAState):
    """
    Validate the question before sending it to the LLM.
    If empty or invalid, provide an error message.
    """
    question = state.get("question", "").strip()
    if not question:
        state["answer"] = "Error: Question cannot be empty."
        # Skip further nodes by ending the workflow here
        state["_end"] = True
    return state

def generate_answer(state: QAState):
    # If validation marked the workflow to end, skip LLM
    if state.get("_end"):
        return state

    llm = ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    prompt = f"Question: {state['question']}\nAnswer:"
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state

def show_result(state: QAState):
    return state

# -------------------------
# LangGraph Workflow
# -------------------------
workflow = StateGraph(QAState)
workflow.add_node("validate", validate_question)
workflow.add_node("answer", generate_answer)
workflow.add_node("result", show_result)

workflow.set_entry_point("validate")
workflow.add_edge("validate", "answer")
workflow.add_edge("answer", "result")
workflow.add_edge("result", END)

app_graph = workflow.compile()

# -------------------------
# FastAPI Endpoint
# -------------------------
class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(req: QuestionRequest):
    state = app_graph.invoke({"question": req.question})
    return {"question": req.question, "answer": state["answer"]}
