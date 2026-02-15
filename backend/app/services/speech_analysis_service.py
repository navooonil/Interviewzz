from typing import List, Dict

# Speech Analysis Metrics
# -----------------------
# This service file contains functions to analyze speech patterns
# based on word-level timestamps provided by the transcription service.

def calculate_speaking_rate(transcript_segments: List[Dict]) -> float:
    """
    Computes the speaking rate in Words Per Minute (WPM).
    
    Formula: (Total Words / Total Duration in Seconds) * 60
    Why it matters: Too fast = nervous/rushed. Too slow = unprepared/hesitant.
    """
    total_words = 0
    total_duration = 0.0
    
    if not transcript_segments:
        return 0.0
        
    start_time = transcript_segments[0]["start"]
    end_time = transcript_segments[-1]["end"]
    total_duration = end_time - start_time
    
    for segment in transcript_segments:
        total_words += len(segment.get("words", []))
        
    if total_duration <= 0:
        return 0.0
        
    wpm = (total_words / total_duration) * 60
    return round(wpm, 2)

def detect_pauses(transcript_segments: List[Dict], min_pause_duration: float = 0.5) -> Dict:
    """
    Identifies gaps between words that are longer than `min_pause_duration`.
    
    Why it matters: Long pauses can indicate thinking, hesitation, or lack of confidence.
    But strategic pauses can emphasize points.
    """
    pauses = []
    total_pause_duration = 0.0
    
    all_words = []
    # Flatten the segments into a single list of words for easier analysis
    for segment in transcript_segments:
        all_words.extend(segment.get("words", []))
        
    if not all_words:
        return {"count": 0, "total_duration": 0.0, "details": []}
        
    for i in range(len(all_words) - 1):
        current_word_end = all_words[i]["end"]
        next_word_start = all_words[i+1]["start"]
        
        gap = next_word_start - current_word_end
        
        if gap > min_pause_duration:
            pauses.append({
                "start": current_word_end,
                "end": next_word_start,
                "duration": round(gap, 2)
            })
            total_pause_duration += gap
            
    return {
        "count": len(pauses),
        "total_duration": round(total_pause_duration, 2),
        "details": pauses
    }

def count_filler_words(transcript_segments: List[Dict]) -> Dict:
    """
    Counts occurrences of common filler words.
    
    Why it matters: Frequent use of 'um', 'uh', 'like' reduces credibility and clarity.
    """
    filler_words_list = {"um", "uh", "er", "ah", "like", "you know", "i mean", "sort of"}
    detected_fillers = {}
    total_count = 0
    
    for segment in transcript_segments:
        for word_data in segment.get("words", []):
            word = word_data["word"].lower().strip(".,?!")
            
            if word in filler_words_list:
                detected_fillers[word] = detected_fillers.get(word, 0) + 1
                total_count += 1
                
    return {
        "total_count": total_count,
        "breakdown": detected_fillers
    }

def analyze_speech(transcription_result: Dict) -> Dict:
    """
    Main function to run all analysis metrics on the transcription result.
    """
    segments = transcription_result.get("segments", [])
    
    return {
        "speaking_rate_wpm": calculate_speaking_rate(segments),
        "pause_analysis": detect_pauses(segments),
        "filler_words": count_filler_words(segments)
    }
