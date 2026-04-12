from env import QADEEnv
from models import QADEAction

tasks = ["bull_trend", "noisy_market", "shock_recovery"]
first_rewards = {}

for task_name in tasks:
    env = QADEEnv(task=task_name)
    obs = env.reset()
    # Check price history instead of reward on step 1
    # Because a HOLD with 0 shares always gives reward=0.12
    price_sig = obs.price_history[-5:]
    first_rewards[task_name] = str(price_sig)
    print(f"{task_name}: price signature = {price_sig}")

# Check all different
vals = list(first_rewards.values())
if len(set(vals)) == len(vals):
    print("\nPASS All tasks produce different price series — seeds are unique")
else:
    print("\nFAIL DUPLICATE PRICE SERIES DETECTED — seeds are failing!")
    print("Check np.random.seed logic in env.py.")
