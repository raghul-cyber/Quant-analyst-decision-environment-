def safe_score(score: float) -> float:
    """
    Clamps a score strictly between 0 and 1 using a very small buffer (0.01).
    Ensures compliance with exclusive interval (0, 1) requirements.
    """
    EPSILON = 0.01
    # Exclusive range: (0.000001, 0.99)
    return max(EPSILON, min(float(score), 1.0 - EPSILON))

