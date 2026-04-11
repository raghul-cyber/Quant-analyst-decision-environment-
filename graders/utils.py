import math


def safe_score(score: float) -> float:
    """
    Clamps a score strictly between 0 and 1.
    Uses 0.001 / 0.999 bounds so even :.2f formatting stays safe.
    """
    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0.001

    if math.isnan(score) or math.isinf(score):
        return 0.001

    if score <= 0.0:
        return 0.001
    if score >= 1.0:
        return 0.99

    return score
