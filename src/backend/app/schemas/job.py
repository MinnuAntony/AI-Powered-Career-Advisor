from pydantic import BaseModel
from typing import Optional

class JobMarketInsight(BaseModel):
    career: str
    demand: str
    avg_salary: Optional[str] = None
    future_outlook: Optional[str] = None

class JobMarketResponse(BaseModel):
    insights: JobMarketInsight
