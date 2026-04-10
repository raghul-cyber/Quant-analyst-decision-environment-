def safe_score(score: float) -> float:
    """
    Clamps a score strictly between 0 and 1 using a small buffer.
    Ensures compliance with exclusive interval (0, 1) requirements.
    """
    EPSILON = 0.001
    return max(EPSILON, min(float(score), 1 - EPSILON))
