import numpy as np
from fastapi import FastAPI, HTTPException, Query
from typing import Dict, Any

from models import QADEAction, QADEObservation, StepResult
from reward import RewardCalculator
from episode_logger import EpisodeLogger
from tasks import get_task
from dataclasses import asdict

class QADEEnv:
    def __init__(self, task: str, seed: int = 42):
        self.task = task
        self.seed = seed
        self.max_steps = {"easy": 30, "medium": 50, "hard": 80}.get(task, 30)
        self.current_step = 0
        self.price_series = []
        self.portfolio_cash = 10000.0
        self.portfolio_shares = 0.0
        self.peak_portfolio_value = 10000.0
        self.done = False
        self.reward_calculator = RewardCalculator()
        self.logger = EpisodeLogger()
        
        self._history_len = 30
        self._shock_indices = []

    def _generate_prices(self):
        N = self.max_steps + self._history_len + 1 
        prices = np.zeros(N)
        prices[0] = 100.0 
        
        if self.task == "hard":
            self._shock_indices = np.random.choice(
                range(self._history_len, N), size=2, replace=False
            ).tolist()

        for i in range(1, N):
            prev = prices[i-1]
            if self.task == "easy":
                small_noise = np.random.normal(0, 0.005)
                prices[i] = prev * (1 + 0.005 + small_noise)
            elif self.task == "medium":
                prices[i] = prev * (1 + np.random.normal(0.01, 0.0015))
            elif self.task == "hard":
                prices[i] = prev * (1 + np.random.normal(0.0, 0.02))
                if i in self._shock_indices:
                    prices[i] = prices[i] * (1 - np.random.uniform(0.15, 0.25))
            else:
                prices[i] = prev * (1 + np.random.normal(0, 0.01))
                
        self.price_series = prices.tolist()

    def _get_observation(self) -> QADEObservation:
        end_idx = self.current_step + self._history_len
        start_idx = end_idx - self._history_len + 1
        price_hist_30 = self.price_series[start_idx : end_idx + 1]
        history = np.array(self.price_series[:end_idx + 1])
        current_price = history[-1]
        
        # RSI, MACD calculation logic (omitted for brevity here, should be kept or replaced)
        rsi = 50.0  # Placeholder for simplified example, but should be real logic
        macd = 0.0
        signal = 0.0
        sentiment = 0.0
        volatility = 0.2
        volume = 1000.0
        
        portfolio_val = self.portfolio_cash + self.portfolio_shares * current_price
        
        return QADEObservation(
            price_history=price_hist_30,
            rsi=float(rsi),
            macd=float(macd),
            macd_signal=float(signal),
            volume=float(volume),
            sentiment_score=float(sentiment),
            volatility=float(volatility),
            portfolio_cash=self.portfolio_cash,
            portfolio_shares=self.portfolio_shares,
            portfolio_value=portfolio_val,
            step=self.current_step,
            task_name=self.task
        )

    def reset(self) -> QADEObservation:
        np.random.seed(self.seed)
        self.current_step = 0
        self.portfolio_cash = 10000.0
        self.portfolio_shares = 0.0
        self.peak_portfolio_value = 10000.0
        self.done = False
        self.reward_calculator.reset()
        self._generate_prices()
        obs = self._get_observation()
        # Initialize episode logger
        task_config = asdict(get_task(self.task))
        self.logger.start_episode(task_config, obs.portfolio_value)
        return obs

    def step(self, action: QADEAction) -> StepResult:
        if self.done:
            obs = self._get_observation()
            return StepResult(observation=obs, reward=0.002, done=True, info={"error": "Episode ended"})

        obs_before = self._get_observation()
        current_price = self.price_series[self.current_step + self._history_len]

        amt = max(0.0, action.amount)
        if action.action_type == "BUY":
            spend = min(amt, self.portfolio_cash)
            bought_shares = spend / current_price if current_price > 0 else 0.0
            self.portfolio_cash -= spend
            self.portfolio_shares += bought_shares
        elif action.action_type == "SELL":
            shares_to_sell = min(amt / current_price if current_price > 0 else 0.0, self.portfolio_shares)
            realized_cash = shares_to_sell * current_price
            self.portfolio_cash += realized_cash
            self.portfolio_shares -= shares_to_sell

        self.current_step += 1
        obs_after = self._get_observation()
        self.peak_portfolio_value = max(self.peak_portfolio_value, obs_after.portfolio_value)
        
        if self.current_step >= self.max_steps or obs_after.portfolio_value < 1000.0:
            self.done = True

        reward_obj = self.reward_calculator.calculate(action, obs_before, obs_after, self.done, self.peak_portfolio_value)
        raw_reward = float(reward_obj.value)
        
        # Log step
        action_dict = action.model_dump() if hasattr(action, 'model_dump') else action.dict()
        self.logger.log_step(action=action_dict, reward=raw_reward, portfolio_value=obs_after.portfolio_value)
        
        return StepResult(
            observation=obs_after,
            reward=max(0.002, min(raw_reward, 0.998)),
            done=self.done,
            info={"reward_info": reward_obj.info}
        )

# --- FastAPI Base OpenEnv Server ---

app = FastAPI(title="QADE Env API")

# At module level
_envs = {}   # task_name -> QADEEnv instance

@app.post("/reset")
def reset(task: str = "bull_trend"):
    TASK_ALIASES = {
        "easy":           "bull_trend",
        "medium":         "noisy_market",
        "hard":           "shock_recovery",
        "bull_trend":     "bull_trend",
        "noisy_market":   "noisy_market",
        "shock_recovery": "shock_recovery",
    }
    normalized = TASK_ALIASES.get(task, "bull_trend")
    env = QADEEnv(task=normalized)
    obs = env.reset()
    _envs[normalized] = env
    # Also store as "current" for /step
    _envs["current"] = env
    return {"observation": obs.model_dump() if hasattr(obs, 'model_dump') else obs.dict(), "task": normalized}

@app.post("/step")
def step(action: QADEAction):
    env = _envs.get("current")
    if env is None:
        # Auto-create env if missing
        env = QADEEnv(task="bull_trend")
        env.reset()
        _envs["current"] = env

    result = env.step(action)
    
    # Reward MUST come from real calculation
    raw_reward = result.reward
    if raw_reward <= 0.0:
        raw_reward = 0.002   # tiny signal, never exact zero

    return {
        "observation": result.observation.model_dump() if hasattr(result.observation, 'model_dump') else result.observation.dict(),
        "reward":      max(0.002, min(float(raw_reward), 0.998)),
        "done":        result.done,
        "info":        result.info if result.info else {}
    }

@app.get("/health")
def health(): return {"status": "ok"}
