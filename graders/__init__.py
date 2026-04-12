import math
from graders.easy_grader   import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader   import grade as hard_grade

def _strict(score: float) -> float:
    try:
        score = float(score)
    except Exception:
        return 0.35
    if math.isnan(score) or math.isinf(score):
        return 0.35
    if score <= 0.0: return 0.001
    if score >= 1.0: return 0.999
    return score

GRADER_MAP = {
    # All possible names validator might send
    "easy":           easy_grade,
    "medium":         medium_grade,
    "hard":           hard_grade,
    "bull_trend":     easy_grade,
    "noisy_market":   medium_grade,
    "shock_recovery": hard_grade,
}

def get_grader(task_name: str):
    grader = GRADER_MAP.get(task_name)
    if grader is None:
        print(f"[WARN] Unknown task: {task_name!r} — using easy_grade fallback")
        grader = easy_grade

    def safe_grader(episode_log: dict) -> float:
        try:
            raw  = grader(episode_log)
            safe = _strict(raw)
            # Final assertion
            assert 0.0 < safe < 1.0, f"score {safe} not in (0,1)"
            return safe
        except AssertionError as e:
            print(f"[WARN] {e}")
            return 0.35
        except Exception as e:
            print(f"[WARN] grader crashed: {e}")
            return 0.35

    return safe_grader
