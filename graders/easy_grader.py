import math

def strict_final(score: float) -> float:
    """
    CRITICAL: OpenEnv rejects exactly 0.0 and exactly 1.0.
    This is the last line of defense before returning.
    """
    try:
        score = float(score)
    except Exception:
        return 0.35
    if math.isnan(score) or math.isinf(score):
        return 0.35
    if score <= 0.0:
        return 0.001
    if score >= 1.0:
        return 0.999
    return score

def grade(episode_log: dict) -> float:
    actions          = episode_log.get("actions", [])
    portfolio_values = episode_log.get("portfolio_values", [])
    final_value      = float(episode_log.get("final_portfolio_value", 10000.0))
    initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0))

    # Safety: no data at all
    if not portfolio_values or initial_value <= 0:
        return 0.35

    # Component 1: Return score (50%)
    pnl_pct      = (final_value - initial_value) / initial_value
    return_score  = pnl_pct / 0.10
    return_score  = strict_final(return_score)

    # Component 2: Direction accuracy (50%)
    correct = 0
    total   = 0
    for i, action in enumerate(actions):
        if i + 1 >= len(portfolio_values):
            break
        total   += 1
        went_up  = portfolio_values[i + 1] > portfolio_values[i]
        atype    = action.get("action_type", "HOLD")
        if (atype == "BUY" and went_up) or \
           (atype in ("SELL", "HOLD") and not went_up):
            correct += 1

    direction_score = (correct / total) if total > 0 else 0.35
    direction_score = strict_final(direction_score)

    final_score = 0.5 * return_score + 0.5 * direction_score
    return strict_final(final_score)
