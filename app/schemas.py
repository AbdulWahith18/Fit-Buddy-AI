"""Pydantic schemas used to validate form and JSON input."""
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    user_id: str = Field(min_length=1, max_length=50, pattern=r"^[A-Za-z0-9_.\-]+$")
    age: int = Field(ge=10, le=100)
    weight: float = Field(gt=20, le=400, description="Weight in kg")
    goal: str = Field(min_length=2, max_length=60)
    intensity: Literal["low", "medium", "high"]

    @field_validator("username", "user_id", "goal", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("intensity", mode="before")
    @classmethod
    def _lower(cls, v):
        return v.strip().lower() if isinstance(v, str) else v


class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=50)
    feedback: str = Field(min_length=3, max_length=1000)

    @field_validator("user_id", "feedback", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v


class PlanOut(BaseModel):
    user_id: str
    username: str
    age: int
    weight: float
    goal: str
    intensity: str
    original_plan: Optional[str] = None
    updated_plan: Optional[str] = None
    feedback: Optional[str] = None
    nutrition_tip: Optional[str] = None


class TipOut(BaseModel):
    goal: str
    nutrition_tip: str
