def _clamp(score: float) -> float:
    score = float(score)
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

    if not portfolio_values or initial_value <= 0:
        return 0.35

    # Component 1: Profit score (40%)
    pnl_pct      = (final_value - initial_value) / initial_value
    profit_score  = _clamp(pnl_pct / 0.05)

    # Component 2: Drawdown control (40%)
    peak         = initial_value
    max_drawdown = 0.0001   # start non-zero to avoid division edge case

    for val in portfolio_values:
        if val > peak:
            peak = val
        if peak > 0:
            dd           = (peak - val) / peak
            max_drawdown = max(max_drawdown, dd)

    # 15% drawdown = 0.001 score
    drawdown_score = 1.0 - (max_drawdown / 0.15)
    drawdown_score = _clamp(drawdown_score)

    # Component 3: Trade efficiency (20%)
    n_trades = sum(
        1 for a in actions
        if a.get("action_type", "HOLD") in ("BUY", "SELL")
    )
    # cap at 20 trades, always non-zero
    efficiency_score = _clamp(1.0 - (n_trades / 20))

    final_score = (
        0.40 * profit_score +
        0.40 * drawdown_score +
        0.20 * efficiency_score
    )
    return _clamp(final_score)
