from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.interview import InterviewCreate, InterviewResponse
from ..services import interview_service

# What is APIRouter?
# APIRouter helps us organize our API routes into different modules.
# We can define prefixed routes here and include them in main.py later.
router = APIRouter()

@router.get("/example", response_model=List[InterviewResponse])
def get_interviews_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of interviews.
    
    This route shows how to use dependency injection for database sessions.
    Also, how to use service functions to keep the logic clean.
    """
    interviews = interview_service.get_interviews(db, skip=skip, limit=limit)
    return interviews

@router.post("/example", response_model=InterviewResponse)
def create_new_interview(interview: InterviewCreate, db: Session = Depends(get_db)):
    """
    Create a new interview.
    
    Validates data using the Pydantic schema (InterviewCreate).
    Uses the service layer to interact with the database.
    """
    return interview_service.create_interview(db, interview.dict())
