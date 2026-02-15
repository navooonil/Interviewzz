from fastapi import APIRouter, HTTPException
from ..schemas.analysis import AnalysisRequest, AnalysisResponse
from ..services.semantic_analysis_service import analyze_semantic_relevance

router = APIRouter()

@router.post("/relevance", response_model=AnalysisResponse)
async def semantic_analysis(request: AnalysisRequest):
    """
    Analyzes the semantic relevance between an interview transcript and a resume.
    
    Logic:
    1. Chunks the interview transcript into 30s segments.
    2. Embeds both the transcript chunks and the resume sections using Sentence Transformers.
    3. Calculates cosine similarity to determine relevance, topic drift, and redundancy.
    """
    try:
        # Check if transcript has valid segments
        if not request.transcript.get("segments"):
            raise HTTPException(status_code=400, detail="Transcript is empty or malformed.")
            
        result = analyze_semantic_relevance(request.transcript, request.resume_text)
        
        if "error" in result:
             raise HTTPException(status_code=400, detail=result["error"])
             
        return result
        
    except Exception as e:
        # In production, log the error here
        raise HTTPException(status_code=500, detail=f"Semantic analysis failed: {str(e)}")
