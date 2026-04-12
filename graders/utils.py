def strict_final(score):
    try:
        score = float(score)
    except:
        return 0.001

    import math
    if math.isnan(score) or math.isinf(score):
        return 0.001

    # HARD FINAL CLAMP (MOST IMPORTANT LINE)
    if score <= 0:
        return 0.001
    if score >= 1:
        return 0.999

    # EXTRA SAFETY (avoid rounding to 1)
    if score > 0.999:
        return 0.999
    if score < 0.001:
        return 0.001

    return score


def strict_safe(score):
    """Alias for backward compatibility if needed, but redirects to strict_final."""
    return strict_final(score)
