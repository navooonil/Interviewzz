from sqlalchemy.orm import Session
from ..models.interview import Interview

# Introduction to Services:
# Services handle the core business logic of the application.
# They interact with the database and perform any necessary data processing.
# Services are used by API routes to keep routes clean and focused on HTTP.

def get_interviews(db: Session, skip: int = 0, limit: int = 100):
    """
    Service function to fetch 
    all interviews from the database.
    
    Args:
        db (Session): The database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Number of records to return (for pagination).
    """
    return db.query(Interview).offset(skip).limit(limit).all()

def create_interview(db: Session, interview_data: dict):
    """
    Service function to create a new interview.
    
    Args:
        db (Session): The database session.
        interview_data (dict): The data (title, etc.) for the new interview.
    """
    # Create a new Interview object
    new_interview = Interview(**interview_data)
    
    # Add to session and commit (save)
    db.add(new_interview)
    db.commit()
    
    # Refresh to update with any DB-generated fields (like ID)
    db.refresh(new_interview)
    return new_interview
