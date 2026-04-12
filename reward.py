from models import QADEAction, QADEObservation, QADEReward

class RewardCalculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.consecutive_wins = 0

    def calculate(self, action, obs_before, obs_after, done, peak_value):
        pnl_delta = obs_after.portfolio_value - obs_before.portfolio_value
        
        # Base reward from pnl — normalize to small range
        if obs_before.portfolio_value > 0:
            pnl_pct    = pnl_delta / obs_before.portfolio_value
            base_reward = pnl_pct * 10.0   # scale so 1% move = 0.1 reward
        else:
            base_reward = 0.0

        # Cap base reward
        base_reward = max(-0.5, min(base_reward, 0.5))

        # Penalties
        total_penalty = 0.0
        if action.action_type in ("BUY", "SELL") and action.amount > 0:
            total_penalty += 0.02   # trade friction

        # Drawdown penalty
        if peak_value > 0:
            drawdown = (peak_value - obs_after.portfolio_value) / peak_value
            if drawdown > 0.05:
                total_penalty += min(drawdown * 1.0, 0.3)

        # Useless action penalty
        if action.action_type == "BUY" and obs_before.portfolio_cash < 10:
            total_penalty += 0.1
        if action.action_type == "SELL" and obs_before.portfolio_shares < 0.001:
            total_penalty += 0.1

        # Bonus
        total_bonus = 0.0
        if pnl_delta > 0:
            self.consecutive_wins += 1
            if self.consecutive_wins >= 3:
                total_bonus += min(0.05 * self.consecutive_wins, 0.2)
        else:
            self.consecutive_wins = 0

        # CRITICAL: add step existence signal
        # This guarantees reward is NEVER exactly 0.0
        EXISTENCE_SIGNAL = 0.05
        
        final_reward = EXISTENCE_SIGNAL + base_reward - total_penalty + total_bonus

        # Hard clamp — strictly open interval
        final_reward = max(0.002, min(final_reward, 0.998))

        return QADEReward(
            value=final_reward,
            pnl_delta=pnl_delta,
            penalty=total_penalty,
            bonus=total_bonus,
            info=f"base={base_reward:.3f} pen={total_penalty:.3f} bon={total_bonus:.3f}"
        )
