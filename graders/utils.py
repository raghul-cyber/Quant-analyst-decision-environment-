import math


def safe_score(score: float) -> float:
    """
    Clamps a score strictly between 0 and 1.
    Uses 0.05 / 0.95 bounds so NO formatting can ever produce 0.00 or 1.00.
    """
    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0.05

    if math.isnan(score) or math.isinf(score):
        return 0.05

    if score <= 0.0:
        return 0.05
    if score >= 1.0:
        return 0.95

    # Extra guard: if it's dangerously close to boundaries
    if score < 0.05:
        return 0.05
    if score > 0.95:
        return 0.95

    return score
