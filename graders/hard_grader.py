def _clamp(score: float) -> float:
    return max(0.001, min(score, 0.999))

def grade(episode_log: dict) -> float:
    portfolio_values = episode_log.get("portfolio_values", [])
    final_value      = episode_log.get("final_portfolio_value", 10000.0)
    initial_value    = episode_log.get("initial_portfolio_value", 10000.0)
    task_config      = episode_log.get("task_config", {})

    shock_steps = task_config.get("shock_steps", [25, 55])

    # --- Component 1: Survival score (30% weight) ---
    # Portfolio must stay above 5000 at ALL times
    min_value      = min(portfolio_values) if portfolio_values else 0.0
    survived       = min_value >= 5000.0
    # Do NOT use 1.0 or 0.0 — use 0.999 and 0.001
    survival_score = 0.999 if survived else 0.001

    # --- Component 2: Recovery score (40% weight) ---
    recovery_scores = []

    for shock_step in shock_steps:
        # value at shock moment
        if shock_step < len(portfolio_values):
            val_at_shock = portfolio_values[shock_step]
        else:
            recovery_scores.append(0.001)
            continue

        # value 10 steps after shock
        recovery_step = shock_step + 10
        if recovery_step < len(portfolio_values):
            val_after_recovery = portfolio_values[recovery_step]
        else:
            val_after_recovery = portfolio_values[-1]

        if val_at_shock <= 0:
            recovery_scores.append(0.001)
            continue

        ratio = val_after_recovery / val_at_shock
        # ratio > 1 means recovered, clamp to open interval
        recovery_scores.append(max(0.001, min(ratio - 0.001, 0.999)))

    recovery_score = sum(recovery_scores) / max(len(recovery_scores), 1)
    recovery_score = max(0.001, min(recovery_score, 0.999))

    # --- Component 3: Final PnL (30% weight) ---
    if initial_value <= 0:
        pnl_score = 0.001
    else:
        pnl_pct   = (final_value - initial_value) / initial_value
        # 3% return = full score
        pnl_score = max(0.001, min(pnl_pct / 0.03, 0.999))

    # --- Final score ---
    final_score = (
        0.30 * survival_score +
        0.40 * recovery_score +
        0.30 * pnl_score
    )

    return _clamp(final_score)
