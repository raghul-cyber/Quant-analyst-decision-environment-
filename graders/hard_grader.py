import math

def _clamp(score) -> float:
    try:
        score = float(score)
    except Exception:
        return 0.50
    if math.isnan(score) or math.isinf(score):
        return 0.50
    score = round(score, 4)          # kill floating point creep
    return max(0.01, min(score, 0.99))

def grade(episode_log: dict) -> float:
    try:
        final       = float(episode_log.get("final_portfolio_value", 10000))
        initial     = float(episode_log.get("initial_portfolio_value", 10000))
        values      = episode_log.get("portfolio_values", [])
        task_config = episode_log.get("task_config", {})
        shock_steps = task_config.get("shock_steps", [25, 55])

        if initial <= 0 or not values:
            return 0.50

        min_val = min(float(v) for v in values)
        s_score = _clamp(min_val / max(float(initial), 1.0))

        r_scores = []
        for ss in shock_steps:
            idx_s = min(int(ss), len(values)-1)
            idx_r = min(int(ss)+10, len(values)-1)
            vs    = float(values[idx_s])
            vr    = float(values[idx_r])
            if vs <= 0:
                r_scores.append(0.50)
                continue
            ratio  = vr / vs
            mapped = (ratio - 0.8) / 0.4
            r_scores.append(_clamp(mapped))
        rec = _clamp(sum(r_scores)/len(r_scores)) if r_scores else 0.50

        pnl     = (final - initial) / initial
        p_score = _clamp((pnl + 0.03) / 0.06)

        return _clamp(0.3*s_score + 0.4*rec + 0.3*p_score)
    except Exception:
        return 0.50
