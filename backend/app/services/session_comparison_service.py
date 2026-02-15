from typing import List, Dict, Any, Optional
import math

# --- SCORING WEIGHTS ---
# We define these constants to make the scoring logic transparent and easy to tune.
# Total must sum to 1.0
WEIGHT_RELEVANCE = 0.40      # Content is King (40%)
WEIGHT_STABILITY = 0.30      # Confidence matters (30%)
WEIGHT_PACE = 0.15           # Speaking rate (15%)
WEIGHT_CLARITY = 0.15        # Filler words (15%)

# --- BENCHMARKS ---
# Used for normalization. These are "ideal" ranges based on public speaking best practices.
IDEAL_WPM_MIN = 120
IDEAL_WPM_MAX = 160
MAX_FILLERS_PER_MIN = 10     # Above this is "bad" (score -> 0)
IDEAL_FILLERS_PER_MIN = 2    # Below this is "perfect" (score -> 1)


def calculate_session_score(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes a single 'Performance Score' (0-100) for an interview session
    by normalizing and weighting individual metrics.
    
    Args:
        metrics: Dictionary containing:
            - overall_relevance (0.0 - 1.0)
            - overall_emotional_stability_score (0.0 - 1.0)
            - speaking_rate_wpm (float)
            - filler_words_count (int)
            - duration_seconds (float)
            
    Returns:
        Dict containing the final score and the breakdown of component scores.
    """
    
    # 1. Normalize Relevance (already 0-1)
    score_relevance = metrics.get('overall_relevance', 0.0)
    
    # 2. Normalize Stability (already 0-1)
    score_stability = metrics.get('overall_emotional_stability_score', 0.0)
    
    # 3. Normalize Speaking Pace (Bell Curve Approximation)
    wpm = metrics.get('speaking_rate_wpm', 0)
    if wpm == 0:
        score_pace = 0.0
    elif IDEAL_WPM_MIN <= wpm <= IDEAL_WPM_MAX:
        score_pace = 1.0
    else:
        # Distance from ideal range
        if wpm < IDEAL_WPM_MIN:
            distance = IDEAL_WPM_MIN - wpm
        else:
            distance = wpm - IDEAL_WPM_MAX
        
        # Penalize: lose 0.02 score for every 1 WPM off. Min score 0.
        penalty = distance * 0.02
        score_pace = max(0.0, 1.0 - penalty)
        
    # 4. Normalize Clarity (Filler Words)
    # Convert absolute count to rate (per minute)
    duration_min = metrics.get('duration_seconds', 0) / 60.0
    if duration_min <= 0:
        fillers_per_min = 0 # Prevent div by zero
    else:
        fillers_per_min = metrics.get('filler_words_count', 0) / duration_min
        
    if fillers_per_min <= IDEAL_FILLERS_PER_MIN:
        score_clarity = 1.0
    elif fillers_per_min >= MAX_FILLERS_PER_MIN:
        score_clarity = 0.0
    else:
        # Linear interpolation between ideal (1.0) and max (0.0)
        # range = 8 (10 - 2)
        score_clarity = 1.0 - ((fillers_per_min - IDEAL_FILLERS_PER_MIN) / (MAX_FILLERS_PER_MIN - IDEAL_FILLERS_PER_MIN))

    # 5. Compute Weighted Score
    final_score = (
        (score_relevance * WEIGHT_RELEVANCE) +
        (score_stability * WEIGHT_STABILITY) +
        (score_pace * WEIGHT_PACE) +
        (score_clarity * WEIGHT_CLARITY)
    ) * 100  # Scale to 0-100 for display
    
    return {
        "final_score": round(final_score, 1),
        "components": {
            "relevance": round(score_relevance * 100, 1),
            "stability": round(score_stability * 100, 1),
            "pace": round(score_pace * 100, 1),
            "clarity": round(score_clarity * 100, 1)
        }
    }

def compare_sessions(current_session: Dict, previous_session: Optional[Dict]) -> Dict[str, Any]:
    """
    Compares the current session against a previous one to identify trends.
    """
    current_results = calculate_session_score(current_session)
    
    if not previous_session:
        return {
            "current_score": current_results["final_score"],
            "trend": "baseline", # First session
            "delta": 0,
            "message": "First session recorded. Baseline established."
        }
        
    previous_results = calculate_session_score(previous_session)
    
    delta = current_results["final_score"] - previous_results["final_score"]
    
    # Define thresholds for meaningful change
    if delta > 5.0:
        trend = "improving"
        msg = "Great job! You represent a significant improvement."
    elif delta < -5.0:
        trend = "declining"
        msg = "Performance dropped compared to last time. Check your stability."
    else:
        trend = "stagnant"
        msg = "Consistent performance. Try to focus on clarity to break through."
        
    return {
        "current_score": current_results["final_score"],
        "previous_score": previous_results["final_score"],
        "trend": trend,
        "delta": round(delta, 1),
        "message": msg,
        "component_breakdown": current_results["components"]
    }
