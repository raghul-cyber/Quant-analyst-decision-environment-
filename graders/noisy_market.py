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
        values  = episode_log.get("portfolio_values", [])
        actions = episode_log.get("actions", [])

        if initial <= 0:
            return 0.50

        pnl     = (final - initial) / initial
        p_score = _clamp((pnl + 0.05) / 0.10)

        peak   = float(initial)
        max_dd = 0.001
        for v in values:
            v = float(v)
            if v > peak:
                peak = v
            if peak > 0:
                max_dd = max(max_dd, (peak - v) / peak)
        d_score = _clamp(0.95 - (max_dd / 0.15))

        n       = sum(1 for a in actions
                      if a.get("action_type","HOLD") in ("BUY","SELL"))
        e_score = _clamp(0.95 - (min(n, 29) / 30))

        return _clamp(0.4*p_score + 0.4*d_score + 0.2*e_score)
    except Exception:
        return 0.50
