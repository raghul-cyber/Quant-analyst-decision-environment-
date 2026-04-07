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
        """Generates the future deterministic price chart ahead of time using numpy"""
        N = self.max_steps + self._history_len + 1 
        prices = np.zeros(N)
        prices[0] = 100.0 
        
        if self.task == "hard":
            # Select 2 shock drop locations out of bounds of the initial burn-in phase
            self._shock_indices = np.random.choice(
                range(self._history_len, N), size=2, replace=False
            ).tolist()

        for i in range(1, N):
            prev = prices[i-1]
            if self.task == "easy":
                small_noise = np.random.normal(0, 0.005)
                prices[i] = prev * (1 + 0.005 + small_noise)
            elif self.task == "medium":
                prices[i] = prev * (1 + np.random.normal(0.001, 0.015))
            elif self.task == "hard":
                prices[i] = prev * (1 + np.random.normal(0.0, 0.02))
                if i in self._shock_indices:
                    # Random shock event 15-25% drop
                    prices[i] = prices[i] * (1 - np.random.uniform(0.15, 0.25))
            else:
                prices[i] = prev * (1 + np.random.normal(0, 0.01))
                
        self.price_series = prices.tolist()

    def _calculate_ema(self, series: np.ndarray, period: int) -> np.ndarray:
        """Fast vectorized proxy loop over an array for exact Exponential Moving Averages"""
        if len(series) == 0:
            return np.array([])
        ema = np.zeros_like(series)
        alpha = 2.0 / (period + 1.0)
        ema[0] = series[0]
        for i in range(1, len(series)):
            ema[i] = alpha * series[i] + (1 - alpha) * ema[i-1]
        return ema

    def _get_observation(self) -> QADEObservation:
        end_idx = self.current_step + self._history_len
        start_idx = end_idx - self._history_len + 1
        
        # We need the last exactly 30 closing prices 
        price_hist_30 = self.price_series[start_idx : end_idx + 1]
        
        history = np.array(self.price_series[:end_idx + 1])
        current_price = history[-1]
        prev_price = history[-2] if len(history) > 1 else current_price
        price_change_pct = (current_price - prev_price) / prev_price if prev_price > 0 else 0.0

        # RSI (14-period standard equivalent matching pandas RS implementation structure natively)
        deltas = np.diff(history)
        rsi = 50.0
        if len(deltas) >= 14:
            recent_deltas = deltas[-14:]
            gains = np.sum(recent_deltas[recent_deltas > 0]) / 14.0
            losses = -np.sum(recent_deltas[recent_deltas < 0]) / 14.0
            if losses == 0:
                rsi = 100.0
            elif gains == 0:
                rsi = 0.0
            else:
                rs = gains / losses
                rsi = 100.0 - (100.0 / (1 + rs))

        # MACD (12 EMA - 26 EMA) -> Signal is 9 EMA of the difference matrix
        if len(history) >= 26:
            ema12 = self._calculate_ema(history, 12)
            ema26 = self._calculate_ema(history, 26)
            macd_series = ema12 - ema26
            macd = macd_series[-1]
            signal = self._calculate_ema(macd_series, 9)[-1]
        else:
            macd = 0.0
            signal = 0.0

        # Seed local internal generator against step so it guarantees reproducible but varied results without global seed manipulation 
        local_rng = np.random.RandomState(self.seed + self.current_step)
        volume = 1000.0 * (1.0 + abs(price_change_pct)*10.0) * local_rng.uniform(0.8, 1.2)

        # Environment sentiment proxy map
        sentiment = 0.0
        if self.task == "easy":
            sentiment = 0.8 if price_change_pct >= 0 else -0.8
        elif self.task == "medium":
            sentiment = local_rng.uniform(-1.0, 1.0)
        elif self.task == "hard":
            sentiment = local_rng.uniform(-0.5, 0.5)
            # Inverse / highly polarized shock correlations 
            if price_change_pct < -0.10:
                sentiment = 1.0 
            elif price_change_pct > 0.10:
                sentiment = -1.0
        
        sentiment = max(-1.0, min(1.0, sentiment))
        
        portfolio_val = self.portfolio_cash + self.portfolio_shares * current_price
        
        # Volatility map
        volatility = 0.2
        if len(history) > 1:
            recent_prices = history[-30:]
            rets = np.diff(recent_prices) / recent_prices[:-1]
            if len(rets) > 0 and np.std(rets) > 0:
                volatility = float(np.std(rets) * np.sqrt(252))

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
        # Apply global numpy seed reset exactly as requested
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
            return StepResult(observation=obs, reward=0.0, done=True, info={"error": "Episode ended"})

        obs_before = self._get_observation()
        
        end_idx = self.current_step + self._history_len
        current_price = self.price_series[end_idx]

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
        elif action.action_type == "HOLD":
            pass

        self.current_step += 1
        obs_after = self._get_observation()
        
        self.peak_portfolio_value = max(self.peak_portfolio_value, obs_after.portfolio_value)
        
        if self.current_step >= self.max_steps or obs_after.portfolio_value < 1000.0:
            self.done = True

        reward = self.reward_calculator.calculate(action, obs_before, obs_after, self.done)
        
        # Log step into episode tracker
        action_dict = action.model_dump() if hasattr(action, 'model_dump') else action.dict()
        self.logger.log_step(
            action=action_dict,
            reward=reward.value,
            portfolio_value=obs_after.portfolio_value
        )
        
        info_dict = {"reward_info": reward.info}
        
        if self.done:
            ep_log = self.logger.end_episode()
            info_dict["episode_log"] = ep_log
        
        return StepResult(
            observation=obs_after,
            reward=reward.value,
            done=self.done,
            info=info_dict
        )
        
    def state(self) -> Dict[str, Any]:
        return {
            "task": self.task,
            "seed": self.seed,
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "portfolio_cash": self.portfolio_cash,
            "portfolio_shares": self.portfolio_shares,
            "peak_portfolio_value": self.peak_portfolio_value,
            "done": self.done,
            "price_series_len": len(self.price_series),
            "history_len": self._history_len
        }


# --- FastAPI Base OpenEnv Server ---

app = FastAPI(title="QADE Env API", description="OpenEnv server for QADE quantitative analytics and testing logic.")

envs: Dict[str, QADEEnv] = {
    "easy": QADEEnv("easy"),
    "medium": QADEEnv("medium"),
    "hard": QADEEnv("hard")
}

@app.post("/reset", response_model=QADEObservation)
def reset_endpoint(task: str = "easy"):
    if task not in envs:
        raise HTTPException(status_code=400, detail="Invalid task configuration mapping requested.")
    return envs[task].reset()

@app.post("/step", response_model=StepResult)
def step_endpoint(action: QADEAction, task: str = Query("easy")):
    if task not in envs:
        raise HTTPException(status_code=400, detail="Invalid task configuration mapping requested.")
    return envs[task].step(action)

@app.get("/state")
def state_endpoint(task: str = "easy"):
    if task not in envs:
        raise HTTPException(status_code=400, detail="Invalid task configuration mapping requested.")
    return envs[task].state()

@app.get("/health")
def health_endpoint():
    return {"status": "ok"}

@app.get("/episodes")
def episodes_endpoint(task: str = Query("easy")):
    if task not in envs:
        raise HTTPException(status_code=400, detail="Invalid task configuration mapping requested.")
    return envs[task].logger.get_last_episodes()
