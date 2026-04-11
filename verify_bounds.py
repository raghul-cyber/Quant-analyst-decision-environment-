import sys
import os

sys.path.insert(0, os.path.abspath("."))

from graders import get_grader


def verify():
    tasks = ["bull_trend", "noisy_market", "shock_recovery", "easy", "medium", "hard"]

    # Empty/Failed log
    failed_log = {
        "actions": [],
        "portfolio_values": [],
        "final_portfolio_value": 0,
        "initial_portfolio_value": 10000.0,
        "task_config": {}
    }

    # Perfect/High log
    perfect_log = {
        "actions": [{"action_type": "BUY"} for _ in range(10)],
        "portfolio_values": [10000.0 * (1 + 0.05 * i) for i in range(11)],
        "final_portfolio_value": 20000.0,
        "initial_portfolio_value": 10000.0,
        "task_config": {"shock_steps": [2, 5]}
    }

    all_pass = True
    for task in tasks:
        print(f"\n--- Testing Grader: {task} ---")
        grader = get_grader(task)

        for name, log in [("FAILED", failed_log), ("PERFECT", perfect_log)]:
            try:
                score = grader(log)
                # Format the same way the validator would see it
                formatted_2f = f"{score:.2f}"
                formatted_6f = f"{score:.6f}"

                print(f"  [{name}] Raw={score}  .2f={formatted_2f}  .6f={formatted_6f}")

                if not (0.0 < score < 1.0):
                    print(f"  [FAIL] Score {score} is not strictly between 0 and 1!")
                    all_pass = False
                elif formatted_2f == "0.00" or formatted_2f == "1.00":
                    print(f"  [FAIL] .2f formatting produces boundary: {formatted_2f}")
                    all_pass = False
                else:
                    print(f"  [PASS]")
            except Exception as e:
                print(f"  [CRASHED] {e}")
                all_pass = False

    if all_pass:
        print("\nALL BOUNDS VERIFIED")
        sys.exit(0)
    else:
        print("\nVERIFICATION FAILED")
        sys.exit(1)


if __name__ == "__main__":
    verify()
