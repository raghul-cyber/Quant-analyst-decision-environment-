import sys
import os

sys.path.insert(0, os.path.abspath("."))

from graders import get_grader


def verify():
    tasks = ["bull_trend", "noisy_market", "shock_recovery", "easy", "medium", "hard"]

    failed_log = {
        "actions": [],
        "portfolio_values": [],
        "final_portfolio_value": 0,
        "initial_portfolio_value": 10000.0,
        "task_config": {}
    }

    perfect_log = {
        "actions": [{"action_type": "BUY"} for _ in range(10)],
        "portfolio_values": [10000.0 * (1 + 0.05 * i) for i in range(11)],
        "final_portfolio_value": 20000.0,
        "initial_portfolio_value": 10000.0,
        "task_config": {"shock_steps": [2, 5]}
    }

    all_pass = True
    for task in tasks:
        print(f"\n--- {task} ---")
        grader = get_grader(task)

        for name, log in [("FAILED", failed_log), ("PERFECT", perfect_log)]:
            try:
                score = grader(log)
                f2 = f"{score:.2f}"
                f6 = f"{score:.6f}"

                if not (0.0 < score < 1.0):
                    print(f"  [{name}] FAIL: raw={score} out of (0,1)")
                    all_pass = False
                elif f6 == "0.000000" or f6 == "1.000000":
                    print(f"  [{name}] FAIL: .6f is boundary")
                    all_pass = False
                else:
                    print(f"  [{name}] PASS  raw={score}  .2f={f2}  .6f={f6}")
            except Exception as e:
                print(f"  [{name}] CRASHED: {e}")
                all_pass = False

    if all_pass:
        print("\nALL BOUNDS VERIFIED - SAFE")
    else:
        print("\nFAILED")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    verify()
