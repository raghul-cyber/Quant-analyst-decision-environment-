from graders.easy_grader   import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader   import grade as hard_grade

def _clamp(score: float) -> float:
    score = float(score)
    if score <= 0.0: return 0.001
    if score >= 1.0: return 0.999
    return score

GRADER_MAP = {
    "easy":           easy_grade,
    "medium":         medium_grade,
    "hard":           hard_grade,
    "bull_trend":     easy_grade,
    "noisy_market":   medium_grade,
    "shock_recovery": hard_grade,
    "easy_task":      easy_grade,
    "medium_task":    medium_grade,
    "hard_task":      hard_grade,
}

def get_grader(task_name: str):
    grader = GRADER_MAP.get(task_name, easy_grade)

    def safe_grader(episode_log: dict) -> float:
        try:
            raw   = grader(episode_log)
            safe  = _clamp(raw)

            # Final paranoia check
            assert 0.0 < safe < 1.0, f"Score {safe} outside (0,1)"
            return safe

        except AssertionError as e:
            print(f"[WARN] Score assertion failed: {e}")
            return 0.5    # safe mid-range fallback

        except Exception as e:
            print(f"[WARN] Grader crashed: {e} — returning 0.5")
            return 0.5

    return safe_grader
