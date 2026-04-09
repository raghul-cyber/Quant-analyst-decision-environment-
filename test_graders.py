from graders import get_grader

EDGE_CASE_LOGS = [
    # Case 1: Zero profit (most likely to produce 0.0)
    {
        "actions": [],
        "rewards": [0.0, 0.0, 0.0],
        "portfolio_values": [10000, 10000, 10000],
        "final_portfolio_value": 10000.0,
        "initial_portfolio_value": 10000.0,
        "steps_taken": 3,
        "task_config": {"shock_steps": [1, 2]}
    },
    # Case 2: Perfect profit (most likely to produce 1.0)
    {
        "actions": [{"action_type": "BUY", "amount": 9000}] * 30,
        "rewards": [5.0] * 30,
        "portfolio_values": [10000 + i * 500 for i in range(31)],
        "final_portfolio_value": 25000.0,
        "initial_portfolio_value": 10000.0,
        "steps_taken": 30,
        "task_config": {"shock_steps": [1, 2]}
    },
    # Case 3: Total loss (most likely to produce 0.0)
    {
        "actions": [{"action_type": "SELL", "amount": 500}] * 10,
        "rewards": [-5.0] * 10,
        "portfolio_values": [10000 - i * 800 for i in range(11)],
        "final_portfolio_value": 2000.0,
        "initial_portfolio_value": 10000.0,
        "steps_taken": 10,
        "task_config": {"shock_steps": [1, 2]}
    },
    # Case 4: Empty log (edge case)
    {
        "actions": [],
        "rewards": [],
        "portfolio_values": [],
        "final_portfolio_value": 10000.0,
        "initial_portfolio_value": 10000.0,
        "steps_taken": 0,
        "task_config": {"shock_steps": [25, 55]}
    },
]

tasks = ["easy", "medium", "hard"]
all_pass = True

for task in tasks:
    grader = get_grader(task)
    for i, log in enumerate(EDGE_CASE_LOGS):
        score = grader(log)
        valid = 0.0 < score < 1.0
        status = "✅" if valid else "❌ FAIL"
        print(f"{status} [{task}] case={i+1} score={score:.6f}")
        if not valid:
            all_pass = False

print()
if all_pass:
    print("🟢 ALL EDGE CASES PASS — Safe to push.")
else:
    print("🔴 SCORES OUT OF RANGE — Fix before pushing!")

