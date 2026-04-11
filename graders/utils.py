def strict_safe(score):
    try:
        score = float(score)
    except:
        return 0.01

    import math
    if math.isnan(score) or math.isinf(score):
        return 0.01

    # HARD CLAMP (STRICT) - Using 0.01/0.99 to avoid any rounding to 0/1
    if score <= 0.01:
        return 0.01
    if score >= 0.99:
        return 0.99

    return score
