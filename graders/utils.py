def strict_final(score):
    try:
        score = float(score)
    except:
        return 0.50

    import math
    if math.isnan(score) or math.isinf(score):
        return 0.50

    # HARD FINAL CLAMP (Standardized to 0.05)
    if score <= 0:
        return 0.05
    if score >= 1:
        return 0.95

    # EXTRA SAFETY (avoid rounding to 1 or 0)
    if score > 0.95:
        return 0.95
    if score < 0.05:
        return 0.05

    return round(score, 4)


def strict_safe(score):
    """Alias for backward compatibility if needed, but redirects to strict_final."""
    return strict_final(score)
