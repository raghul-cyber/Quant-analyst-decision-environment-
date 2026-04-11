from graders.utils import safe_score


def grade(episode_log: dict) -> float:
    try:
        actions          = episode_log.get("actions", [])
        portfolio_values = episode_log.get("portfolio_values", [])
        final_value      = float(episode_log.get("final_portfolio_value", 10000.0) or 10000.0)
        initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0) or 10000.0)

        if not portfolio_values or initial_value <= 0:
            return 0.5

        # Component 1: Profit score (40%)
        pnl_pct      = (final_value - initial_value) / initial_value
        profit_score  = safe_score(pnl_pct / 0.05)

        # Component 2: Drawdown control (40%)
        peak         = initial_value
        max_drawdown = 0.0001

        for val in portfolio_values:
            if val > peak:
                peak = val
            if peak > 0:
                dd           = (peak - val) / peak
                max_drawdown = max(max_drawdown, dd)

        drawdown_score = 1.0 - (max_drawdown / 0.15)
        drawdown_score = safe_score(drawdown_score)

        # Component 3: Trade efficiency (20%)
        n_trades = 0
        for a in actions:
            if isinstance(a, dict):
                act_type = a.get("action_type", "HOLD")
            elif isinstance(a, str):
                act_type = a
            else:
                act_type = "HOLD"

            if act_type in ("BUY", "SELL"):
                n_trades += 1

        efficiency_score = safe_score(1.0 - (n_trades / 20))

        final_score = (
            0.40 * profit_score +
            0.40 * drawdown_score +
            0.20 * efficiency_score
        )
        return safe_score(final_score)
    except Exception:
        return 0.05
