def grade(episode_log: dict) -> float:
    actions = episode_log.get("actions", [])
    portfolio_values = episode_log.get("portfolio_values", [])
    final = episode_log.get("final_portfolio_value", 0.0)
    initial = episode_log.get("initial_portfolio_value", 10000.0)
    steps = episode_log.get("steps_taken", 0)

    # 1. Return score (50% weight)
    pnl_pct = (final - initial) / initial if initial > 0 else 0.0
    return_score = min(max(pnl_pct / 0.10, 0.0), 1.0)  # 10% return = full score

    # 2. Direction score (50% weight)
    # count steps where action was BUY and portfolio went up, or HOLD/SELL and it went down
    if steps == 0 or len(portfolio_values) < 2:
        return 0.5 * return_score
    
    correct_steps = 0
    # Safe guard on iteration length vs actions list
    limit = min(steps, len(actions), len(portfolio_values) - 1)
    
    for t in range(limit):
        act_type = actions[t].get("action_type")
        val_before = portfolio_values[t]
        val_after = portfolio_values[t+1]
        went_up = val_after > val_before
        
        if act_type == "BUY" and went_up:
            correct_steps += 1
        elif act_type in ["SELL", "HOLD"] and not went_up:
            correct_steps += 1

    direction_score = correct_steps / limit if limit > 0 else 0.0
    
    return 0.5 * return_score + 0.5 * direction_score
