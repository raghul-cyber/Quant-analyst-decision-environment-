import math

def strict_final(score: float) -> float:
    try:
        score = float(score)
    except Exception:
        return 0.35
    if math.isnan(score) or math.isinf(score):
        return 0.35
    if score <= 0.0: return 0.001
    if score >= 1.0: return 0.999
    return score

def grade(episode_log: dict) -> float:
    portfolio_values = episode_log.get("portfolio_values", [])
    final_value      = float(episode_log.get("final_portfolio_value", 10000.0))
    initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0))
    task_config      = episode_log.get("task_config", {})
    shock_steps      = task_config.get("shock_steps", [25, 55])

    if not portfolio_values or initial_value <= 0:
        return 0.35

    # Component 1: Survival (30%)
    min_val = min(portfolio_values)
    if min_val >= 5000.0:
        survival_score = 0.8 + (min_val / initial_value) * 0.1  # dynamic, never round 0.85
    else:
        survival_score = strict_final(min_val / 5000.0 * 0.5)

    # Component 2: Recovery (40%)
    recovery_scores = []
    for shock_step in shock_steps:
        idx_s = min(shock_step, len(portfolio_values) - 1)
        idx_r = min(shock_step + 10, len(portfolio_values) - 1)
        v_s   = portfolio_values[idx_s]
        v_r   = portfolio_values[idx_r]
        if v_s <= 0:
            recovery_scores.append(0.1)
            continue
        ratio  = v_r / v_s
        mapped = (ratio - 0.8) / 0.4
        recovery_scores.append(strict_final(mapped))

    recovery_score = sum(recovery_scores) / max(len(recovery_scores), 1)
    recovery_score = strict_final(recovery_score)

    # Component 3: PnL (30%)
    pnl_pct   = (final_value - initial_value) / initial_value
    pnl_score = strict_final(pnl_pct / 0.03)

    final_score = (
        0.30 * survival_score +
        0.40 * recovery_score +
        0.30 * pnl_score
    )
    return strict_final(final_score)
