def _clamp(score: float) -> int:
    try:
        score = float(score)
    except Exception:
        return 0
    if score >= 0:
        return 1
    return 0

def grade(episode_log: dict) -> float:
    try:
        portfolio_values = episode_log.get("portfolio_values", [])
        final_value      = float(episode_log.get("final_portfolio_value", 10000.0) or 10000.0)
        initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0) or 10000.0)
        task_config      = episode_log.get("task_config", {}) or {}
        shock_steps      = task_config.get("shock_steps", [25, 55])

        if not portfolio_values or initial_value <= 0:
            return 0

        # Component 1: Survival (30%)
        min_value = min(portfolio_values)
        if min_value >= 5000.0:
            survival_score = 0.95   # good but not 1.0
        else:
            # partial credit based on how low it went
            survival_score = _clamp(min_value / 5000.0 * 0)

        # Component 2: Recovery (40%)
        recovery_scores = []
        for shock_step in shock_steps:
            idx_shock    = min(shock_step, len(portfolio_values) - 1)
            idx_recovery = min(shock_step + 10, len(portfolio_values) - 1)

            val_shock    = portfolio_values[idx_shock]
            val_recovery = portfolio_values[idx_recovery]

            if val_shock <= 0:
                recovery_scores.append(0.1)
                continue

            ratio = val_recovery / val_shock
            # ratio of 1.0 = no recovery, ratio > 1.0 = recovered
            # map: 0.8 ratio -> 0.1, 1.0 ratio -> 0, 1.2 ratio -> 0.9
            mapped = (ratio - 0.8) / 0.4    # 0.8..1.2 maps to 0.0..1.0
            recovery_scores.append(_clamp(mapped))

        recovery_score = sum(recovery_scores) / max(len(recovery_scores), 1)
        recovery_score = _clamp(recovery_score)

        # Component 3: Final PnL (30%)
        pnl_pct   = (final_value - initial_value) / initial_value
        pnl_score = _clamp(pnl_pct / 0.03)

        final_score = (
            0.30 * survival_score +
            0.40 * recovery_score +
            0.30 * pnl_score
        )
        return _clamp(final_score)
    except Exception:
        return 0

