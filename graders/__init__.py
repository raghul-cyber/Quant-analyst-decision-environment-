from graders.easy_grader   import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader   import grade as hard_grade
from graders.utils import strict_safe

GRADER_MAP = {
    "easy":           easy_grade,
    "medium":         medium_grade,
    "hard":           hard_grade,
    "bull_trend":     easy_grade,
    "noisy_market":   medium_grade,
    "shock_recovery": hard_grade,
}

def get_grader(task_name: str):
    grader = GRADER_MAP.get(task_name, easy_grade)

    def safe_grader(episode_log: dict) -> float:
        try:
            raw = grader(episode_log)
            return strict_safe(raw)
        except Exception as e:
            print(f"[WARN] Grader crashed: {e}")
            return 0.001

    return safe_grader
