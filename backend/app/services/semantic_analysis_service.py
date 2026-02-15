import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

# Global variable to hold the model instance (Singleton pattern)
# We load this once to avoid high latency on every request.
# 'all-MiniLM-L6-v2' is a fast, lightweight, and high-performance model for semantic similarity.
_model = None

def get_model():
    """
    Lazy-loads the Sentence Transformer model.
    This ensures we only load the heavy model when we actually need it.
    """
    global _model
    if _model is None:
        print("Loading Semantic Model (all-MiniLM-L6-v2)...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully.")
    return _model

def chunk_transcript(transcript_segments: List[Dict], chunk_duration: int = 30) -> List[Dict]:
    """
    Groups individual transcript segments/words into larger time-based chunks.
    
    Why: Individual sentences might not have enough context.
    30-second chunks allow us to analyze a complete "thought" or "answer".
    
    Args:
        transcript_segments (list): The granular segments from Whisper (usually word-level or phrase-level).
        chunk_duration (int): Duration in seconds for each chunk.
    
    Returns:
        List[Dict]: A list of chunk objects with start_time, end_time, and combined text.
    """
    chunks = []
    
    if not transcript_segments:
        return chunks
        
    current_chunk_text = []
    chunk_start_time = transcript_segments[0].get("start", 0)
    current_chunk_end = 0
    
    for segment in transcript_segments:
        # We assume the segment has 'start', 'end', and 'text'
        start = segment.get("start", 0)
        end = segment.get("end", 0)
        text = segment.get("text", "").strip()
        
        # If this segment starts after our current chunk window, close the current chunk
        if start - chunk_start_time >= chunk_duration:
            # Finalize the previous chunk
            if current_chunk_text:
                chunks.append({
                    "timestamp": f"{int(chunk_start_time)}s - {int(current_chunk_end)}s",
                    "start": chunk_start_time,
                    "end": current_chunk_end,
                    "text": " ".join(current_chunk_text)
                })
            
            # Start a new chunk
            current_chunk_text = [text]
            chunk_start_time = start
            current_chunk_end = end
        else:
            # Continue adding to the current chunk
            current_chunk_text.append(text)
            current_chunk_end = end
            
    # Don't forget the last chunk
    if current_chunk_text:
        chunks.append({
            "timestamp": f"{int(chunk_start_time)}s - {int(current_chunk_end)}s",
            "start": chunk_start_time,
            "end": current_chunk_end,
            "text": " ".join(current_chunk_text)
        })
        
    return chunks

def segment_resume(resume_text: str) -> List[str]:
    """
    Breaks a plain text resume into logical sections.
    
    Simple Heuristic: Split by double newlines (\n\n) which usually separate paragraphs
    or sections in plain text resumes.
    """
    # Remove excessive whitespace and split
    sections = [s.strip() for s in resume_text.split('\n\n') if s.strip()]
    return sections

def compute_similarity(text_list_1: List[str], text_list_2: List[str]) -> np.ndarray:
    """
    Computes the cosine similarity matrix between two lists of strings.
    
    How it works:
    1. Convert texts to Vector Embeddings (lists of numbers representing meaning).
    2. Compute Cosine Similarity (angle between vectors).
       1.0 = Identical meaning
       0.0 = Unrelated
    """
    model = get_model()
    
    # 1. Encode text into embeddings
    # embeddings_1 shape: (num_texts_1, embedding_dim)
    embeddings_1 = model.encode(text_list_1)
    embeddings_2 = model.encode(text_list_2)
    
    # 2. Compute Cosine Similarity
    # Result is a matrix of shape (num_texts_1, num_texts_2)
    return cosine_similarity(embeddings_1, embeddings_2)

def analyze_semantic_relevance(transcript_data: Dict, resume_text: str) -> Dict[str, Any]:
    """
    Main orchestration function for semantic analysis.
    
    1. Chunks the interview into 30s segments.
    2. Segments the resume.
    3. Compares each interview chunk against ALL resume sections.
    4. Calculates Topic Drift and Redundancy.
    """
    # 1. Prepare Data
    chunks = chunk_transcript(transcript_data.get("segments", []), chunk_duration=30)
    resume_sections = segment_resume(resume_text)
    
    if not chunks or not resume_sections:
        return {"error": "Insufficient data for analysis"}

    model = get_model()
    
    # Pre-compute text lists specifically for embedding
    chunk_texts = [c["text"] for c in chunks]
    
    # --- A. Relevance Analysis (Interview vs Resume) ---
    # We compare every chunk to every resume section to find the "best match"
    similarity_matrix = compute_similarity(chunk_texts, resume_sections)
    
    # Update chunks with relevance scores
    for i, chunk in enumerate(chunks):
        # extraction row i from matrix (this chunks correlation with all resume sections)
        similarities = similarity_matrix[i]
        
        # Max score = how well this chunk matches the *most relevant* part of the resume
        best_match_idx = np.argmax(similarities)
        max_score = similarities[best_match_idx]
        
        chunk["relevance_score"] = round(float(max_score), 2)
        chunk["matched_resume_section"] = resume_sections[best_match_idx][:100] + "..." # Snippet
        
    # --- B. Topic Drift (Chunk vs Previous Chunk) ---
    # We compare chunk[i] with chunk[i-1] to see if the conversation flows logically
    # Low similarity might indicate a sudden topic switch (Drift).
    chunk_embeddings = model.encode(chunk_texts)
    drift_scores = []
    
    # We start from index 1 since 0 has no previous chunk
    for i in range(1, len(chunks)):
        # Reshape for sklearn (1, dim)
        current_emb = chunk_embeddings[i].reshape(1, -1)
        prev_emb = chunk_embeddings[i-1].reshape(1, -1)
        
        sim = cosine_similarity(current_emb, prev_emb)[0][0]
        drift_scores.append(round(float(sim), 2))
        
        chunks[i]["coherence_with_prev"] = round(float(sim), 2)
        
    # First chunk gets a default value
    if chunks:
        chunks[0]["coherence_with_prev"] = 1.0

    # --- C. Redundancy (Chunk vs All Previous Chunks) ---
    # Check if the candidate is repeating themselves.
    redundancy_alerts = []
    for i in range(1, len(chunks)):
        current_emb = chunk_embeddings[i].reshape(1, -1)
        # Compare with ALL previous chunks (0 to i-1)
        prev_embeddings = chunk_embeddings[:i]
        
        sims = cosine_similarity(current_emb, prev_embeddings)[0]
        max_redundancy = np.max(sims)
        
        chunks[i]["max_redundancy_score"] = round(float(max_redundancy), 2)
        
        if max_redundancy > 0.85: # Threshold for "highly repetitive"
            redundancy_alerts.append({
                "chunk_index": i,
                "timestamp": chunks[i]["timestamp"],
                "message": "Candidate repeated a previously discussed point."
            })
    
    if chunks:
         chunks[0]["max_redundancy_score"] = 0.0

    return {
        "overall_relevance": round(float(np.mean([c["relevance_score"] for c in chunks])), 2),
        "chunk_analysis": chunks,
        "redundancy_alerts": redundancy_alerts,
        "topic_drift_timeline": drift_scores
    }
