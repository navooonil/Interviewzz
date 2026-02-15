import whisper
import os
import shutil
from fastapi import UploadFile, HTTPException
from ..utils.helpers import log_debug_message

# Configuration:
# We are using the "base" model as requested.
MODEL_NAME = "base"

# FORCE FFMPEG PATH (Robust Fix for Windows)
# We search for the ffmpeg binary and add it to PATH programmatically
import glob
local_app_data = os.environ.get("LOCALAPPDATA", "")
ffmpeg_search_path = os.path.join(local_app_data, "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg_*", "ffmpeg-*-full_build", "bin")
found_ffmpeg_dirs = glob.glob(ffmpeg_search_path)

if found_ffmpeg_dirs:
    # Add the first found directory to PATH
    os.environ["PATH"] += os.pathsep + found_ffmpeg_dirs[0]
    log_debug_message(f"Added FFmpeg to PATH: {found_ffmpeg_dirs[0]}")
else:
    log_debug_message("WARNING: Could not auto-locate FFmpeg. Relying on system PATH.")

# Load the Whisper model into memory when this service is imported.
try:
    log_debug_message(f"Loading Whisper model: {MODEL_NAME}...")
    model = whisper.load_model(MODEL_NAME)
    log_debug_message("Whisper model loaded successfully.")
except Exception as e:
    log_debug_message(f"Error loading Whisper model: {e}")
    # We don't crash here, but transcription will fail if model isn't loaded.
    model = None

# Directory to save uploaded files temporarily
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile) -> str:
    """
    Saves an uploaded file to the local disk.
    
    Args:
        upload_file (UploadFile): The file uploaded by the user.
        
    Returns:
        str: The absolute path to the saved file.
    """
    try:
        # Create a safe file path
        file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
        
        # Write the file to disk chunk by chunk to handle large files efficiently
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

def transcribe(file_path: str, cleanup: bool = True):
    """
    Transcribes an audio file and extracts word-level timestamps.
    
    Args:
        file_path (str): Path to the audio file.
        
    Returns:
        dict: Structured transcription data.
    """
    if not model:
        raise HTTPException(status_code=500, detail="Whisper model not loaded.")
        
    try:
        # The core Whisper transcription call
        # word_timestamps=True tells Whisper to extract timing for each word
        result = model.transcribe(file_path, word_timestamps=True)
        
        # Structure the output for the frontend
        # We perform some cleanup to make the JSON cleaner
        structured_output = {
            "full_text": result["text"].strip(),
            "segments": []
        }
        
        for segment in result["segments"]:
            segment_data = {
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip(),
                "words": []
            }
            
            # Extract word-level details if available
            if "words" in segment:
                for word in segment["words"]:
                    segment_data["words"].append({
                        "word": word["word"].strip(),
                        "start": word["start"],
                        "end": word["end"]
                    })
            
            structured_output["segments"].append(segment_data)
            
        return structured_output
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
    finally:
        # Cleanup: Remove the file after processing to save space
        # In a real app, you might want to keep it in S3 or similar.
        if cleanup and os.path.exists(file_path):
            os.remove(file_path)
