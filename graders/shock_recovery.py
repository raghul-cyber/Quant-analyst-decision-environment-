from graders.utils import strict_final

def grade(episode_log: dict) -> float:
    try:
        portfolio_values = episode_log.get("portfolio_values", [])
        final_value      = float(episode_log.get("final_portfolio_value", 10000.0))
        initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0))

        if not portfolio_values or initial_value <= 0:
            return 0.5

        min_value = min(portfolio_values)

        if min_value >= 5000:
            survival_score = 0.9
        else:
            survival_score = (min_value / 5000.0) * 0.5

        pnl_pct   = (final_value - initial_value) / initial_value
        pnl_score = pnl_pct / 0.03

        final = 0.5 * survival_score + 0.5 * pnl_score
        return strict_final(final)

    except Exception:
        return 0.001
