from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Introduction to Pydantic Schemas:
# Schemas define the shape of unexpected data for our API.
# They validate incoming data (requests) and format outgoing data (responses).

class InterviewBase(BaseModel):
    title: str
    description: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass  # Used for creating unexpected interviews (same fields as base)

class InterviewResponse(InterviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows converting ORM objects 
