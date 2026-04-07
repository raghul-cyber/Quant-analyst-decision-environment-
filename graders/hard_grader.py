def grade(episode_log: dict) -> float:
    portfolio_values = episode_log.get("portfolio_values", [])
    final = episode_log.get("final_portfolio_value", 0.0)
    initial = episode_log.get("initial_portfolio_value", 10000.0)

    # 1. Survival score (30% weight)
    survival = 1.0
    for val in portfolio_values:
        if val < 5000:
            survival = 0.0
            break

    # 2. Recovery score (40% weight)
    task_config = episode_log.get("task_config", {})
    shocks = task_config.get("price_params", {}).get("shock_steps", [25, 55])
    
    recovery_sum = 0.0
    valid_shocks = 0
    for shock_step in shocks:
        if shock_step < len(portfolio_values):
            val_start = portfolio_values[shock_step]
            end_step = min(shock_step + 10, len(portfolio_values) - 1)
            val_end = portfolio_values[end_step]
            
            if val_start > 0:
                ratio = val_end / val_start
                # clipped to [0, 1]
                recovery_sum += min(max(ratio, 0.0), 1.0)
            valid_shocks += 1

    recovery_score = recovery_sum / valid_shocks if valid_shocks > 0 else 0.0

    # 3. Final PnL (30% weight)
    # 3% return = full score
    pnl_pct = (final - initial) / initial if initial > 0 else 0.0
    pnl_score = min(max(pnl_pct / 0.03, 0.0), 1.0)

    return 0.3 * survival + 0.4 * recovery_score + 0.3 * pnl_score
