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
    actions          = episode_log.get("actions", [])
    portfolio_values = episode_log.get("portfolio_values", [])
    final_value      = float(episode_log.get("final_portfolio_value", 10000.0))
    initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0))

    if not portfolio_values or initial_value <= 0:
        return 0.35

    # Component 1: Profit (40%)
    pnl_pct      = (final_value - initial_value) / initial_value
    profit_score = strict_final(pnl_pct / 0.05)

    # Component 2: Drawdown (40%)
    peak         = initial_value
    max_dd       = 0.0001
    for val in portfolio_values:
        if val > peak:
            peak = val
        if peak > 0:
            max_dd = max(max_dd, (peak - val) / peak)

    drawdown_score = strict_final(1.0 - (max_dd / 0.15))

    # Component 3: Trade efficiency (20%)
    n_trades = sum(
        1 for a in actions
        if a.get("action_type", "HOLD") in ("BUY", "SELL")
    )
    efficiency_score = strict_final(1.0 - (n_trades / 20))

    final_score = (
        0.40 * profit_score +
        0.40 * drawdown_score +
        0.20 * efficiency_score
    )
    return strict_final(final_score)
