def _clamp(score: float) -> float:
    return max(0.001, min(score, 0.999))

def grade(episode_log: dict) -> float:
    actions          = episode_log.get("actions", [])
    portfolio_values = episode_log.get("portfolio_values", [])
    final_value      = episode_log.get("final_portfolio_value", 10000.0)
    initial_value    = episode_log.get("initial_portfolio_value", 10000.0)

    # --- Component 1: Profit score (40% weight) ---
    if initial_value <= 0:
        profit_score = 0.001
    else:
        pnl_pct      = (final_value - initial_value) / initial_value
        # 5% return = full score
        profit_score = max(0.001, min(pnl_pct / 0.05, 0.999))

    # --- Component 2: Drawdown control (40% weight) ---
    peak         = initial_value
    max_drawdown = 0.0

    for val in portfolio_values:
        if val > peak:
            peak = val
        if peak > 0:
            drawdown     = (peak - val) / peak
            max_drawdown = max(max_drawdown, drawdown)

    # 15% drawdown = 0 score, but clamp away from 0 and 1
    drawdown_score = max(0.001, min(1.0 - max_drawdown / 0.15, 0.999))

    # --- Component 3: Trade efficiency (20% weight) ---
    n_trades = sum(
        1 for a in actions
        if a.get("action_type", "HOLD") in ("BUY", "SELL")
    )
    # More than 20 trades = 0 efficiency, but clamp
    efficiency_score = max(0.001, min(1.0 - n_trades / 20, 0.999))

    # --- Final score ---
    final_score = (
        0.40 * profit_score +
        0.40 * drawdown_score +
        0.20 * efficiency_score
    )

    return _clamp(final_score)
