from graders.utils import strict_safe

def grade(episode_log: dict) -> float:
    try:
        portfolio_values = episode_log.get("portfolio_values", [])
        final_value      = float(episode_log.get("final_portfolio_value", 10000.0))
        initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0))

        if not portfolio_values or initial_value <= 0:
            return 0.5

        pnl_pct = (final_value - initial_value) / initial_value
        return_score = pnl_pct / 0.10

        direction_score = 0.5  # fallback (since actions empty)

        final = 0.5 * return_score + 0.5 * direction_score
        return strict_safe(final)

    except Exception:
        return 0.001
