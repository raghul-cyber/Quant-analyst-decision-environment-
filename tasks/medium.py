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
        name="noisy_market",
        description="Trade in a volatile market with mixed signals",
        max_steps=50,
        initial_cash=10000.0,
        price_params={
            "start_price": 100.0,
            "drift": 0.001,
            "volatility": 0.018,
            "shock_count": 0
        },
        success_threshold=0.45,
        hints=["Market is noisy — manage drawdown", "Don't overtrade"]
    )

