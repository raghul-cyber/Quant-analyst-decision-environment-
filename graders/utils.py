def strict_safe(score):
    try:
        score = float(score)
    except:
        return 0.05

    import math
    if math.isnan(score) or math.isinf(score):
        return 0.05

    # HARD CLAMP (SUPER STRICT)
    # Using 0.05 and 0.9 to ensure average never rounds to 0.0 or 1.0
    if score <= 0.05:
        return 0.05
    if score >= 0.9:
        return 0.9

    return score
