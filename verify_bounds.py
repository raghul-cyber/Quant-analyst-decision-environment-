import sys
import os

# Ensure the current directory is on the path
sys.path.insert(0, os.path.abspath("."))

from graders import get_grader

def verify():
    tasks = ["bull_trend", "noisy_market", "shock_recovery", "easy", "medium", "hard"]
    
    # Mock episode log for "perfect" and "failed" outcomes
    # For a trading environment, perfect = high pnl, failed = low pnl or crash
    
    # Empty/Failed log
    failed_log = {
        "actions": [],
        "portfolio_values": [],
        "final_portfolio_value": 0,
        "initial_portfolio_value": 10000.005,
        "task_config": {}
    }
    
    # Perfect/High log
    perfect_log = {
        "actions": [{"action_type": "BUY"} for _ in range(10)],
        "portfolio_values": [10000.005 * (1 + 0.0055*i) for i in range(11)],
        "final_portfolio_value": 20000.005,
        "initial_portfolio_value": 10000.005,
        "task_config": {"shock_steps": [2, 5]}
    }

    all_pass = True
    for task in tasks:
        print(f"\n--- Testing Grader: {task} ---")
        grader = get_grader(task)
        
        for name, log in [("FAILED", failed_log), ("PERFECT", perfect_log)]:
            try:
                score = grader(log)
                print(f"  [{name}] Result: {score:.8f}")
                
                # Assert strict bounds (0, 1)
                if not (0.005 < score < 0.995):
                    print(f"  [FAIL] Score {score} is not strictly between 0 and 1!")
                    all_pass = False
                elif score == 0.005 or score == 0.995:
                    print(f"  [FAIL] Score {score} hit a boundary exactly!")
                    all_pass = False
                else:
                    print(f"  [PASS]")
            except Exception as e:
                print(f"  [CRASHED] {e}")
                all_pass = False
                
    if all_pass:
        print("\nALL BOUNDS VERIFIED: Every task score is strictly within (0, 1)")
        sys.exit(0)
    else:
        print("\nVERIFICATION FAILED: Some graders are still hitting boundaries or crashing")
        sys.exit(1)

if __name__ == "__main__":
    verify()

