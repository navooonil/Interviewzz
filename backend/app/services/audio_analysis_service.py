import numpy as np
import librosa
from typing import List, Dict, Any

def get_audio_features(file_path: str, transcript_segments: List[Dict]) -> Dict[str, Any]:
    """
    Analyzes emotional stability by measuring prosodic features (pitch and energy) 
    over time, aligned with transcript segments.
    
    Why Stability?
    - High Pitch Variance (uncontrolled) -> Nervousness / Shaky voice
    - Low Pitch Variance -> Monotone / Robotic / Bored
    - High Energy Variance -> Erratic volume control
    - Consistent Energy -> Confident projection
    
    We aim for "Controlled Variance" - expressive but not shaky.
    However, for simplicity, we treat high random variance as "Instability".
    """
    try:
        # Load audio file
        # sr=None preserves the native sampling rate
        y, sr = librosa.load(file_path, sr=None)
        
        # 1. Extract Energy (RMS) - "Loudness"
        # frame_length corresponds to ~50ms windows
        hop_length = 512
        rmse = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop_length)[0]
        
        # 2. Extract Pitch (Fundamental Frequency - F0)
        # We use librosa.pyin (Probabilistic YIN) for robust pitch tracking
        # limit fmin/fmax to human voice range (50Hz - 500Hz covers most speech)
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=50, fmax=500, sr=sr, frame_length=2048, hop_length=hop_length)
        
        # Replace NaNs (unvoiced segments) with 0 for calculation
        f0 = np.nan_to_num(f0)
        
        segment_analysis = []
        overall_pitch_variances = []
        overall_energy_variances = []
        
        # Time per frame in seconds
        frame_time = hop_length / sr
        
        # Analyze each segment from the transcript
        for segment in transcript_segments:
            start_time = segment.get("start", 0)
            end_time = segment.get("end", 0)
            text = segment.get("text", "")
            
            # Convert time to frame indices
            start_frame = int(start_time / frame_time)
            end_frame = int(end_time / frame_time)
            
            # Ensure indices are within bounds
            if start_frame >= len(rmse) or end_frame > len(rmse):
                continue
                
            # Extract features for this segment
            segment_pitch = f0[start_frame:end_frame]
            segment_energy = rmse[start_frame:end_frame]
            
            # Filter out silence/unvoiced parts for pitch calculation
            # We only care about pitch when the person is actually speaking (voiced)
            voiced_pitch = segment_pitch[segment_pitch > 0]
            
            if len(voiced_pitch) > 0:
                pitch_std = np.std(voiced_pitch)
                pitch_mean = np.mean(voiced_pitch)
                # Coefficient of Variation (CV) - Normalized variance
                pitch_stability_score = 1.0 - min(pitch_std / (pitch_mean + 1e-6), 1.0)
            else:
                pitch_std = 0
                pitch_stability_score = 0.5 # Neutral if no voice detected
                
            if len(segment_energy) > 0:
                energy_std = np.std(segment_energy)
                energy_mean = np.mean(segment_energy)
                # Energy stability score
                energy_stability_score = 1.0 - min(energy_std / (energy_mean + 1e-6), 1.0)
            else:
                energy_std = 0
                energy_stability_score = 0.5
                
            overall_pitch_variances.append(pitch_stability_score)
            overall_energy_variances.append(energy_stability_score)
            
            segment_analysis.append({
                "timestamp": f"{round(start_time, 1)}s - {round(end_time, 1)}s",
                "text": text,
                "pitch_stability": round(float(pitch_stability_score), 2),
                "energy_stability": round(float(energy_stability_score), 2),
                "emotional_state": "Stable" if (pitch_stability_score > 0.7 and energy_stability_score > 0.7) else "Variable"
            })
            
        # Calculate overall score (0.0 to 1.0)
        if overall_pitch_variances:
            avg_pitch_stability = np.mean(overall_pitch_variances)
            avg_energy_stability = np.mean(overall_energy_variances)
            overall_score = (avg_pitch_stability + avg_energy_stability) / 2
        else:
            overall_score = 0.0
            
        return {
            "overall_emotional_stability_score": round(float(overall_score), 2),
            "segment_analysis": segment_analysis,
            "metrics": {
                "average_pitch_stability": round(float(np.mean(overall_pitch_variances)), 2) if overall_pitch_variances else 0,
                "average_energy_stability": round(float(np.mean(overall_energy_variances)), 2) if overall_energy_variances else 0
            }
        }

    except Exception as e:
        print(f"Error in audio analysis: {e}")
        return {"error": str(e)}
