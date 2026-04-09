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
        name="shock_recovery",
        description="Survive two sudden market shocks and recover",
        max_steps=80,
        initial_cash=10000.0,
        price_params={
            "start_price": 100.0,
            "drift": 0.002,
            "volatility": 0.020,
            "shock_count": 2,
            "shock_magnitude": -0.20,   # -20% shocks
            "shock_steps": [25, 55]     # shocks happen at these steps
        },
        success_threshold=0.3,
        hints=["Two shocks incoming — protect capital", "Recovery after shocks is rewarded"]
    )

