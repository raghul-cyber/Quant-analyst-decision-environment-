from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class TaskConfig:
    name: str
    description: str
    max_steps: int
    initial_cash: float
    price_params: Dict[str, Any]
    success_threshold: float
    hints: List[str]

def get_task_config() -> TaskConfig:
    return TaskConfig(
        name="bull_trend",
        description="Trade a stock in a clear bull market with low noise",
        max_steps=30,
        initial_cash=10000.0,
        price_params={
            "start_price": 100.0,
            "drift": 0.006,        # strong uptrend
            "volatility": 0.005,   # very low noise
            "shock_count": 0
        },
        success_threshold=0.6,
        hints=["Price is trending up consistently", "Buy early and hold"]
    )
