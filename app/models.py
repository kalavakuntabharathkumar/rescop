from pydantic import BaseModel, Field
from typing import Optional

class DocumentIn(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    text: str = Field(min_length=20, max_length=250_000)
    source: str = "manual"

class ResearchRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=10)

class RiskRequest(BaseModel):
    returns: list[float] = Field(min_length=2, max_length=100_000)
    annualization: int = Field(default=252, ge=1, le=366)
