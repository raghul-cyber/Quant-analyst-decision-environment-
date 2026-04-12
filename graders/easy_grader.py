import math

def _clamp(score) -> float:
    try:
        score = float(score)
    except Exception:
        return 0.50
    if math.isnan(score) or math.isinf(score):
        return 0.50
    score = round(score, 4)          # kill floating point creep
    return max(0.05, min(score, 0.95))

def grade(episode_log: dict) -> float:
    try:
        final   = float(episode_log.get("final_portfolio_value", 10000))
        initial = float(episode_log.get("initial_portfolio_value", 10000))
        actions = episode_log.get("actions", [])
        values  = episode_log.get("portfolio_values", [])

        if initial <= 0:
            return 0.50

        pnl     = (final - initial) / initial
        r_score = _clamp((pnl + 0.10) / 0.20)

        correct = 0
        total   = 0
        for i, action in enumerate(actions):
            if i + 1 >= len(values):
                break
            total += 1
            up    = float(values[i+1]) > float(values[i])
            atype = action.get("action_type", "HOLD")
            if (atype == "BUY" and up) or \
               (atype in ("SELL","HOLD") and not up):
                correct += 1
        d_score = _clamp(correct/total) if total > 0 else 0.50

        return _clamp(0.5 * r_score + 0.5 * d_score)
    except Exception:
        return 0.50
