from tasks import easy, medium, hard
from tasks.easy import TaskConfig

def get_task(name: str) -> TaskConfig:
    """
    Returns the task configuration given its name or difficulty map setting.
    """
    if name in ["bull_trend", "easy"]:
        return easy.get_task_config() # type: ignore
    elif name in ["noisy_market", "medium"]:
        return medium.get_task_config() # type: ignore
    elif name in ["shock_recovery", "hard"]:
        return hard.get_task_config() # type: ignore
    else:
        raise ValueError(f"Unknown task name: {name}")

