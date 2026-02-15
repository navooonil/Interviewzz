from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalysisRequest(BaseModel):
    """
    Schema for the semantic analysis input.
    """
    transcript: Dict[str, Any]  # The full JSON output from the transcription service
    resume_text: str

class AnalysisChunk(BaseModel):
    timestamp: str
    start: float
    end: float
    text: str
    relevance_score: float
    matched_resume_section: str
    coherence_with_prev: float
    max_redundancy_score: float

class RedundancyAlert(BaseModel):
    chunk_index: int
    timestamp: str
    message: str

class AnalysisResponse(BaseModel):
    """
    Schema for the semantic analysis output.
    """
    overall_relevance: float
    chunk_analysis: List[AnalysisChunk]
    redundancy_alerts: List[RedundancyAlert]
    topic_drift_timeline: List[float]
