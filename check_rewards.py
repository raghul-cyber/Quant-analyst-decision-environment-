"""
Run this before every push.
Simulates what the validator does:
Parses [END] line and checks every reward value.
"""
import subprocess
import re
import sys

def check_rewards_in_end_line(end_line: str) -> bool:
    """
    Parse [END] line and verify no reward is 0.0 or 1.0 exactly.
    """
    match = re.search(r'rewards=([^\s]*)', end_line)
    if not match:
        print("❌ No rewards= field found in [END] line")
        return False

    rewards_str = match.group(1)
    if not rewards_str:
        print("⚠️  rewards= is empty — may be ok if 0 steps")
        return True

    rewards = rewards_str.split(",")
    all_ok  = True

    for r_str in rewards:
        try:
            r = float(r_str)
        except ValueError:
            print(f"❌ Cannot parse reward value: {r_str!r}")
            all_ok = False
            continue

        if r == 0.0:
            print(f"❌ FORBIDDEN: reward is exactly 0.0")
            all_ok = False
        elif r == 1.0:
            print(f"❌ FORBIDDEN: reward is exactly 1.0")
            all_ok = False
        elif not (0.0 < r < 1.0):
            print(f"❌ OUT OF RANGE: reward {r} not in (0, 1)")
            all_ok = False
        else:
            print(f"✅ reward {r:.4f} is valid")

    return all_ok

# Simulate a mock [END] line with your actual reward function
# Replace this with actual output from running inference.py
test_cases = [
    "[END] success=true steps=5 rewards=0.001,0.234,0.567,0.891,0.123",  # should PASS
    "[END] success=true steps=3 rewards=0.00,0.50,0.75",                  # should FAIL
    "[END] success=true steps=3 rewards=1.00,0.50,0.75",                  # should FAIL
    "[END] success=false steps=0 rewards=",                                 # edge case
]

print("=== Reward Validator Simulation ===\n")
for line in test_cases:
    print(f"Testing: {line}")
    ok = check_rewards_in_end_line(line)
    print(f"Result: {'PASS' if ok else 'FAIL'}\n")

print("=== Done ===")
print("If all your test cases show PASS, you are safe to push.")
