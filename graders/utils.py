def strict_safe(score):
    try:
        score = float(score)
    except:
        return 0.001

    import math
    if math.isnan(score) or math.isinf(score):
        return 0.001

    # HARD CLAMP (STRICT)
    if score <= 0:
        return 0.001
    if score >= 1:
        return 0.999

    return score
