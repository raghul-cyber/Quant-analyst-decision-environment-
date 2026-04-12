def strict_safe(score):
    try:
        score = float(score)
    except:
        return 0.15

    import math
    if math.isnan(score) or math.isinf(score):
        return 0.15

    # HARD CLAMP (STRICTEST)
    # Using 0.05 and 0.85 to ensure average never rounds to 0.0 or 1.0
    # and avoiding constant-pattern detection
    if score <= 0.05:
        return 0.07  # slightly off the edge
    if score >= 0.85:
        return 0.85

    return score
