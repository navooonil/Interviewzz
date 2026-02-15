from typing import Dict, List, Any

# --- FEEDBACK TEMPLATES ---
# We use templates to ensure consistent, high-quality advice.
FEEDBACK_TEMPLATES = {
    "pace_too_fast": {
        "title": "Slow Down",
        "description": "Your speaking rate is {wpm} words per minute. This is faster than the ideal 120-150 range.",
        "action": "Take a breath between sentences. Rushing can make you seem nervous."
    },
    "pace_too_slow": {
        "title": "Pick Up the Pace",
        "description": "At {wpm} words per minute, your delivery might feel hesitant or low-energy.",
        "action": "Try to practice speaking with a bit more urgency to show enthusiasm."
    },
    "high_fillers": {
        "title": "Reduce Filler Words",
        "description": "You used '{filler}' {count} times. These can distract the interviewer.",
        "action": "Pause silently instead of saying 'um' or 'uh' while thinking."
    },
    "low_relevance": {
        "title": "Stay On Topic",
        "description": "Your answer drifted away from your resume experience ({score}% match).",
        "action": "Connect your answer explicitly back to the skills listed on your resume."
    },
    "low_stability": {
        "title": "Work on Confidence",
        "description": "Your voice variance suggests nervousness or hesitation.",
        "action": "Practice speaking with a steady, consistent volume. Record yourself reading a book aloud."
    },
    "good_job": {
        "title": "Strong Performance",
        "description": "You balanced content, pace, and clarity well.",
        "action": "Keep this up! Focus now on refining your technical depth."
    }
}

def generate_insights(metrics: Dict[str, Any], semantic_score: float, stability_score: float) -> Dict[str, Any]:
    """
    Converts raw numerical metrics into human-readable feedback.
    
    Logic:
    1. Checks each metric against defined thresholds.
    2. Selects the most critical issues (Low Score -> High Priority).
    3. Selects strengths (High Score).
    4. Formats everything into a clear report.
    """
    
    strengths = []
    areas_for_improvement = []
    
    # 1. Analyze Speaking Pace
    wpm = metrics.get('speaking_rate_wpm', 0)
    if wpm > 160:
        areas_for_improvement.append({
            "type": "pace",
            "title": FEEDBACK_TEMPLATES["pace_too_fast"]["title"],
            "message": FEEDBACK_TEMPLATES["pace_too_fast"]["description"].format(wpm=int(wpm)),
            "suggestion": FEEDBACK_TEMPLATES["pace_too_fast"]["action"],
            "priority": "High" if wpm > 180 else "Medium"
        })
    elif wpm < 110:
        areas_for_improvement.append({
            "type": "pace",
            "title": FEEDBACK_TEMPLATES["pace_too_slow"]["title"],
            "message": FEEDBACK_TEMPLATES["pace_too_slow"]["description"].format(wpm=int(wpm)),
            "suggestion": FEEDBACK_TEMPLATES["pace_too_slow"]["action"],
            "priority": "Medium"
        })
    else:
        strengths.append("Perfect speaking pace (120-160 WPM). You sounded natural and controlled.")

    # 2. Analyze Clarity (Fillers)
    fillers = metrics.get('filler_words', {}).get('total_count', 0)
    # Simple heuristic: if fillers are > 5% of total words (approx), highlight it.
    # We'll use absolute count for simplicity here since duration varies.
    if fillers > 8:
         # Find the most frequent filler
         breakdown = metrics.get('filler_words', {}).get('breakdown', {})
         most_used = max(breakdown, key=breakdown.get) if breakdown else "fillers"
         
         areas_for_improvement.append({
            "type": "clarity",
            "title": FEEDBACK_TEMPLATES["high_fillers"]["title"],
            "message": FEEDBACK_TEMPLATES["high_fillers"]["description"].format(filler=most_used, count=fillers),
            "suggestion": FEEDBACK_TEMPLATES["high_fillers"]["action"],
            "priority": "High"
        })
    elif fillers < 3:
        strengths.append("Excellent clarity with very few filler words.")

    # 3. Analyze Semantic Relevance
    if semantic_score < 0.6:
        areas_for_improvement.append({
            "type": "relevance",
            "title": FEEDBACK_TEMPLATES["low_relevance"]["title"],
            "message": FEEDBACK_TEMPLATES["low_relevance"]["description"].format(score=int(semantic_score * 100)),
            "suggestion": FEEDBACK_TEMPLATES["low_relevance"]["action"],
            "priority": "Critical"
        })
    elif semantic_score > 0.85:
        strengths.append("High relevance! Your answer was directly aligned with your resume experience.")

    # 4. Analyze Emotional Stability
    if stability_score < 0.6:
         areas_for_improvement.append({
            "type": "confidence",
            "title": FEEDBACK_TEMPLATES["low_stability"]["title"],
            "message": FEEDBACK_TEMPLATES["low_stability"]["description"],
            "suggestion": FEEDBACK_TEMPLATES["low_stability"]["action"],
            "priority": "High"
        })
    elif stability_score > 0.8:
        strengths.append("You sounded very confident and emotionally stable.")

    # Summary
    if not areas_for_improvement:
        summary = "Outstanding interview! You checked all the boxes for a strong performance."
    elif len(areas_for_improvement) > 3:
        summary = "There are several areas to work on. Focus on slowing down and staying on topic first."
    else:
        summary = "Good effort. With a few tweaks to your delivery, this could be a great answer."

    return {
        "summary": summary,
        "strengths": strengths,
        "improvements": areas_for_improvement,
        "grade": calculate_grade(len(strengths), len(areas_for_improvement))
    }

def calculate_grade(num_strengths: int, num_issues: int) -> str:
    """Simple grading logic based on ratio of good/bad signals."""
    score = num_strengths - (num_issues * 1.5)
    if score >= 3: return "A"
    if score >= 1: return "B"
    if score >= -1: return "C"
    return "D"
