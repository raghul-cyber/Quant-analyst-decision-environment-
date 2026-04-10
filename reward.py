from models import QADEAction, QADEObservation, QADEReward

def _safe_reward(value: float) -> float:
    """
    Ensure reward is strictly between 0 and 1.
    """
    try:
        val = float(value)
    except Exception:
        return 0.000001
    if val <= 0.0: return 0.000001
    if val >= 1.0: return 0.999999
    return val

class RewardCalculator:
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the internal state counters for a new episode."""
        self.peak_value = 0.0
        self.consecutive_wins = 0
        self.consecutive_holds = 0

    def calculate(
        self, 
        action: QADEAction, 
        obs_before: QADEObservation, 
        obs_after: QADEObservation, 
        done: bool
    ) -> QADEReward:
        """
        Calculates the step reward based on the action taken and state transition.
        """
        # Initialize peak value on the first step using obs_before
        if self.peak_value == 0.0:
            self.peak_value = obs_before.portfolio_value
        
        # Update peak portfolio value with the latest observation
        self.peak_value = max(self.peak_value, obs_after.portfolio_value)

        penalty = 0.0
        bonus = 0.0
        info_reasons = []

        # 1. PROFIT SIGNAL
        pnl_delta = obs_after.portfolio_value - obs_before.portfolio_value
        if obs_before.portfolio_value > 0:
            base_reward_raw = (pnl_delta / obs_before.portfolio_value) * 100.0
        else:
            base_reward_raw = 0.0
        
        # Cap base reward to [-5.0, +5.0]
        base_reward = max(-5.0, min(base_reward_raw, 5.0))

        # 2. OVERTRADING PENALTY
        if action.action_type in ("BUY", "SELL") and action.amount > 0:
            penalty += 0.05
            info_reasons.append("overtrading")

        # 3. DRAWDOWN PENALTY
        if self.peak_value > 0:
            current_drawdown = (self.peak_value - obs_after.portfolio_value) / self.peak_value
            if current_drawdown > 0.05:
                penalty += current_drawdown * 2.0
                info_reasons.append("drawdown")

        # 4. USELESS ACTION PENALTY
        if action.action_type == "BUY" and obs_before.portfolio_cash < 10.0:
            penalty += 0.2
            info_reasons.append("useless_buy")
        elif action.action_type == "SELL" and obs_before.portfolio_shares < 0:
            penalty += 0.2
            info_reasons.append("useless_sell")

        # 5. CONSISTENCY BONUS
        if pnl_delta > 0:
            self.consecutive_wins += 1
            if self.consecutive_wins >= 3:
                added_bonus = 0.1 * self.consecutive_wins
                # Cap bonus at 0.5
                added_bonus = min(added_bonus, 0.5)
                bonus += added_bonus
                info_reasons.append(f"consistency_bonus({self.consecutive_wins}w)")
        else:
            self.consecutive_wins = 0

        # 6. HOLD PENALTY (light)
        if action.action_type == "HOLD":
            self.consecutive_holds += 1
            if self.consecutive_holds > 5:
                penalty += 0.05
                info_reasons.append(f"hold_penalty({self.consecutive_holds}h)")
        else:
            self.consecutive_holds = 0

        # Final reward calculation
        # Step existence reward — ensures reward is NEVER exactly 0.0
        STEP_BASE = 0.000001   # tiny reward just for existing

        final_reward = STEP_BASE + base_reward - penalty + bonus
        final_reward = _safe_reward(final_reward)

        # Hard clamp — belt and suspenders
        if final_reward <= 0.0:
            final_reward = 0.000001
        if final_reward >= 1.0:
            final_reward = 0.999999

        # Format info string
        info_str = ", ".join(info_reasons) if info_reasons else "normal_step"

        return QADEReward(
            value=final_reward,
            pnl_delta=pnl_delta,
            penalty=penalty,
            bonus=bonus,
            info=info_str
        )



