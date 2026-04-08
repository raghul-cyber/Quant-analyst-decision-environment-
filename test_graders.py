from graders import get_grader

def make_fake_log(task_name):
    return {
        "actions": [
            {"action_type": "BUY",  "amount": 500.0},
            {"action_type": "HOLD", "amount": 0.0},
            {"action_type": "SELL", "amount": 300.0},
        ],
        "rewards": [0.5, 0.1, -0.2],
        "portfolio_values": [10000, 10200, 10150, 10300],
        "final_portfolio_value": 10300.0,
        "initial_portfolio_value": 10000.0,
        "steps_taken": 3,
        "task_config": {
            "shock_steps": [1, 2]
        }
    }

tasks = ["bull_trend", "noisy_market", "shock_recovery"]

all_pass = True
for task in tasks:
    grader = get_grader(task)
    log    = make_fake_log(task)
    score  = grader(log)

    strictly_valid = 0.0 < score < 1.0
    status = "✅ PASS" if strictly_valid else "❌ FAIL"
    print(f"{status} [{task}] score={score:.6f} | strictly in (0,1): {strictly_valid}")

    if not strictly_valid:
        all_pass = False

print()
if all_pass:
    print("🟢 ALL GRADERS VALID — Safe to push and resubmit.")
else:
    print("🔴 GRADER SCORES OUT OF RANGE — Fix before submitting!")
