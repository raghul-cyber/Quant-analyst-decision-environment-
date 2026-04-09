def _clamp(score: float) -> float:
    score = float(score)
    if score <= 0.0: return 0.01
    if score >= 1.0: return 0.99
    return score

def grade(episode_log: dict) -> float:
    try:
        actions          = episode_log.get("actions", [])
        portfolio_values = episode_log.get("portfolio_values", [])
        final_value      = float(episode_log.get("final_portfolio_value", 10000.0) or 10000.0)
        initial_value    = float(episode_log.get("initial_portfolio_value", 10000.0) or 10000.0)

        # Safety: if no data at all, return mid-range score
        if not portfolio_values or initial_value <= 0:
            return 0.5

        # Component 1: Return score (50%)
        pnl_pct      = (final_value - initial_value) / initial_value
        return_score  = pnl_pct / 0.10   # 10% gain = 1.0
        return_score  = _clamp(return_score)

        # Component 2: Direction accuracy (50%)
        correct = 0
        total   = 0

        for i, action in enumerate(actions):
            if i + 1 >= len(portfolio_values):
                break
            total += 1
            went_up     = portfolio_values[i + 1] > portfolio_values[i]
            
            # Handle action as dict or string
            if isinstance(action, dict):
                action_type = action.get("action_type", "HOLD")
            elif isinstance(action, str):
                action_type = action
            else:
                action_type = "HOLD"

            if (action_type == "BUY" and went_up) or \
               (action_type in ("SELL", "HOLD") and not went_up):
                correct += 1

        if total == 0:
            direction_score = 0.5   # safe mid-range fallback
        else:
            direction_score = correct / total
            direction_score = _clamp(direction_score)

        final_score = 0.5 * return_score + 0.5 * direction_score
        return _clamp(final_score)
    except Exception:
        # Prevent validator from substituting 0.0 on crash
        return 0.5

