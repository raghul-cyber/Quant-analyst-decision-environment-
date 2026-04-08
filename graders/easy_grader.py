def _clamp(score: float) -> float:
    return max(0.001, min(score, 0.999))

def grade(episode_log: dict) -> float:
    actions          = episode_log.get("actions", [])
    rewards          = episode_log.get("rewards", [])
    portfolio_values = episode_log.get("portfolio_values", [])
    final_value      = episode_log.get("final_portfolio_value", 10000.0)
    initial_value    = episode_log.get("initial_portfolio_value", 10000.0)
    steps_taken      = episode_log.get("steps_taken", 1)

    # --- Component 1: Return score (50% weight) ---
    if initial_value <= 0:
        return_score = 0.001
    else:
        pnl_pct      = (final_value - initial_value) / initial_value
        # 10% return = full score, but clamp BEFORE weighting
        return_score = max(0.001, min(pnl_pct / 0.10, 0.999))

    # --- Component 2: Direction score (50% weight) ---
    correct = 0
    total   = max(len(actions), 1)

    for i, action in enumerate(actions):
        if i + 1 >= len(portfolio_values):
            break
        val_before = portfolio_values[i]
        val_after  = portfolio_values[i + 1]
        went_up    = val_after > val_before

        action_type = action.get("action_type", "HOLD")

        if action_type == "BUY" and went_up:
            correct += 1
        elif action_type in ("SELL", "HOLD") and not went_up:
            correct += 1

    direction_score = correct / total
    # clamp component too
    direction_score = max(0.001, min(direction_score, 0.999))

    # --- Final score ---
    final_score = 0.5 * return_score + 0.5 * direction_score

    return _clamp(final_score)
