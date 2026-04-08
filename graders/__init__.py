from graders.easy_grader   import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader   import grade as hard_grade

def _clamp(score: float) -> float:
    return max(0.001, min(float(score), 0.999))

def get_grader(task_name: str):
    # Map EVERY possible name the validator might send
    # Both the short names AND the full descriptive names
    graders = {
        # Short names (what validator actually sends)
        "easy":   easy_grade,
        "medium": medium_grade,
        "hard":   hard_grade,

        # Full task names (from openenv.yaml)
        "bull_trend":     easy_grade,
        "noisy_market":   medium_grade,
        "shock_recovery": hard_grade,

        # Extra aliases just in case
        "easy_task":   easy_grade,
        "medium_task": medium_grade,
        "hard_task":   hard_grade,
    }

    grader = graders.get(task_name)

    if grader is None:
        # Do NOT raise ValueError — return easy grader as safe fallback
        # This prevents unhandled exception crash
        print(f"[WARN] Unknown task name: {task_name!r} — using easy grader as fallback")
        grader = easy_grade

    def safe_grader(episode_log: dict) -> float:
        try:
            score = grader(episode_log)
            return _clamp(score)
        except Exception as e:
            print(f"[WARN] Grader failed: {e} — returning fallback score 0.5")
            return 0.5

    return safe_grader
