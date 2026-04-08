from graders.easy_grader   import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader   import grade as hard_grade

def get_grader(task_name: str):
    graders = {
        "bull_trend":     easy_grade,
        "noisy_market":   medium_grade,
        "shock_recovery": hard_grade,
    }
    grader = graders.get(task_name)
    if grader is None:
        raise ValueError(f"Unknown task: {task_name}")

    # Wrap every grader with a safety net
    def safe_grader(episode_log: dict) -> float:
        score = grader(episode_log)
        # Hard enforce open interval — never let 0.0 or 1.0 through
        score = max(0.001, min(float(score), 0.999))
        assert 0.0 < score < 1.0, f"Grader {task_name} returned invalid score: {score}"
        return score

    return safe_grader
