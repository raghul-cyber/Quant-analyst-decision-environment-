import re, sys, os

SUSPICIOUS_VALUES = [
    "0.700000", "0.720000", "0.750000",
    "0.800000", "0.850000", "0.900000",
    "= 0.12",   "= 0.7",   "= 0.72",
    "= 0.85",   "= 0.9",
    "EXISTENCE_SIGNAL = 0.12",
    "reward = 0.12",
    "reward = 0.7",
]

FILES_TO_CHECK = [
    "inference.py", "env.py", "reward.py",
    "tasks/easy.py", "tasks/medium.py", "tasks/hard.py",
    "graders/shock_recovery.py", "graders/hard_grader.py"
]

found_any = False
for filepath in FILES_TO_CHECK:
    if not os.path.exists(filepath):
        continue
    with open(filepath) as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        for pattern in SUSPICIOUS_VALUES:
            if pattern in line and not line.strip().startswith("#"):
                # Special case: allow 0.7 if it's temperature=0.7
                if "temperature=0.7" in line:
                    continue
                print(f"[FAIL] {filepath}:{i}: {line.rstrip()}")
                found_any = True

if found_any:
    print("\nRED: Hardcoded values found - remove them before pushing!")
    sys.exit(1)
else:
    print("GREEN: No hardcoded reward values found - safe to push")
    sys.exit(0)
