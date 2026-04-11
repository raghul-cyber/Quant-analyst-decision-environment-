from graders.utils import strict_safe

def grade(episode_log: dict) -> float:
    try:
        portfolio_values = episode_log.get("portfolio_values", [])
        final_value      = float(episode_log.get("final_portfolio_value", 10000.0))
        initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0))

        if not portfolio_values or initial_value <= 0:
            return 0.5

        pnl_pct = (final_value - initial_value) / initial_value
        profit_score = pnl_pct / 0.05

        peak = initial_value
        max_drawdown = 0.0

        for val in portfolio_values:
            peak = max(peak, val)
            if peak > 0:
                max_drawdown = max(max_drawdown, (peak - val) / peak)

        drawdown_score = 1 - (max_drawdown / 0.15)

        final = 0.5 * profit_score + 0.5 * drawdown_score
        return strict_safe(final)

    except Exception:
        return 0.001
