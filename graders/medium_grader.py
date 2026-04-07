def grade(episode_log: dict) -> float:
    actions = episode_log.get("actions", [])
    portfolio_values = episode_log.get("portfolio_values", [])
    final = episode_log.get("final_portfolio_value", 0.0)
    initial = episode_log.get("initial_portfolio_value", 10000.0)

    # 1. Profit score (40% weight)
    # 5% return = full score
    pnl_pct = (final - initial) / initial if initial > 0 else 0.0
    profit_score = min(max(pnl_pct / 0.05, 0.0), 1.0)

    # 2. Drawdown control (40% weight)
    # max_drawdown = max drop from peak at any point
    drawdown_score = 1.0
    if portfolio_values:
        peak = portfolio_values[0]
        max_drawdown = 0.0
        for val in portfolio_values:
            if val > peak:
                peak = val
            drawdown = (peak - val) / peak if peak > 0 else 0.0
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                
        # 15% drawdown = 0 score
        drawdown_score = max(0.0, 1.0 - max_drawdown / 0.15)

    # 3. Trade efficiency (20% weight)
    n_trades = sum(1 for a in actions if a.get("action_type") in ["BUY", "SELL"])
    efficiency_score = max(0.0, 1.0 - n_trades / 20.0)

    return 0.4 * profit_score + 0.4 * drawdown_score + 0.2 * efficiency_score
