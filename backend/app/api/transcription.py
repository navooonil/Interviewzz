from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services import transcription_service, speech_analysis_service, audio_analysis_service
from ..services.s3_service import s3_service
import os

router = APIRouter()

SUPPORTED_EXTENSIONS = {".wav", ".mp3", ".m4a"}

@router.post("/transcribe", summary="Upload and Transcribe Audio")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint to upload an audio file and get a timestamped transcription.
    
    1. Validates the file extension.
    2. Saves the file temporarily.
    3. Uses Whisper to transcribe.
    4. Returns the result as JSON.
    """
    
    # 1. Validate File Extension
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()
    
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {extension}. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    
    # 2. Save the file using the service layer
    # We await this if it was async, but shutil is sync.
    # We can run it in a threadpool if blocking becomes an issue, but for now simple sync call is okay.
    file_path = transcription_service.save_upload_file(file)
    
    try:
        # 3. Transcribe audio using the service layer
        # cleanup=False because we need the file for the next step
        transcription_result = transcription_service.transcribe(file_path, cleanup=False)
        
        # 4. Analyze Speech patterns
        analysis_result = speech_analysis_service.analyze_speech(transcription_result)

        # 5. Analyze Emotional Stability (Audio Features)
        emotional_analysis = audio_analysis_service.get_audio_features(file_path, transcription_result.get("segments", []))
        
        # 6. Archive to AWS S3 (Optional)
        # This will only upload if use_s3_storage is True in config
        s3_url = s3_service.upload_file(file_path)

        # Merge results
        return {
            "transcription": transcription_result,
            "analysis": analysis_result,
            "emotional_stability": emotional_analysis,
            "archive_url": s3_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Manual cleanup since we told transcription_service NOT to do it
        if os.path.exists(file_path):
            os.remove(file_path)
