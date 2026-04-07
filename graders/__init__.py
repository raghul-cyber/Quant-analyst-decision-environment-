from typing import Callable
from graders import easy_grader, medium_grader, hard_grader

def get_grader(task_name: str) -> Callable[[dict], float]:
    """
    Returns the grader function grading pipeline given the difficulty specification key.
    """
    if task_name in ["bull_trend", "easy"]:
        return easy_grader.grade
    elif task_name in ["noisy_market", "medium"]:
        return medium_grader.grade
    elif task_name in ["shock_recovery", "hard"]:
        return hard_grader.grade
    else:
        raise ValueError(f"Unknown task name: {task_name}")
