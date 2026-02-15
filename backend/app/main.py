from fastapi import FastAPI
from .api import interviews, transcription, analysis
from .database import engine, Base
from .config import settings
from .utils.helpers import log_debug_message

# Introduction to FastAPI App Initialization:
# This file is the entry point. It creates the FastAPI "app" instance.
# It also includes (registers) routers and configures middleware.

# Create database tables automatically (for development simplicity)
# In production, you would use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Backend API for Interview Performance Analyzer",
    version="0.1.0",
    debug=settings.debug
)

# Include Routers
# Routers handle specific parts of the API (e.g., /interviews).
# This keeps main.py clean and manageable.
app.include_router(interviews.router, prefix="/api/v1/interviews", tags=["interviews"])
app.include_router(transcription.router, prefix="/api/v1/transcription", tags=["transcription"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["semantic-analysis"])

@app.get("/")
def read_root():
    """Simple root endpoint to verify API is running."""
    log_debug_message("Root endpoint called.")
    return {"message": "Welcome to the Interview Performance Analyzer API"}

if __name__ == "__main__":
    import uvicorn
    # Use uvicorn to run the app directly if this file is executed
    uvicorn.run(app, host="0.0.0.0", port=8000)
