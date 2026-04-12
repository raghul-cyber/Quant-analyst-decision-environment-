import re, os, sys

PATTERNS = [
    (r'max\(0\.00[0-9]',  "floor below 0.01 - will round to 0.00"),
    (r'min\(.*0\.99[5-9]',"ceiling above 0.99 - will round to 1.00"),
    (r'= 0\.0[^1-9]',     "value that rounds to 0.0"),
    (r'reward.*= 0\.0\b', "reward set to exactly 0.0"),
    (r'score.*= 0\.0\b',  "score set to exactly 0.0"),
    (r'score.*= 1\.0\b',  "score set to exactly 1.0"),
    (r'return 0\.0\b',    "returning exactly 0.0"),
    (r'return 1\.0\b',    "returning exactly 1.0"),
]

FILES = ["inference.py", "reward.py", "env.py"]
for root, dirs, files in os.walk("graders"):
    for f in files:
        if f.endswith(".py"):
            FILES.append(os.path.join(root, f))

found = False
for filepath in FILES:
    if not os.path.exists(filepath): continue
    with open(filepath, encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except:
            continue
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        for pattern, reason in PATTERNS:
            if re.search(pattern, line):
                # Clean up the line for printing
                safe_stripped = stripped.encode('ascii', errors='replace').decode('ascii')
                print(f"[WARN] {filepath}:{i}: {reason}")
                print(f"   {safe_stripped}")
                found = True

print()
if found:
    print("Fix above findings if they are in return paths or reward/score outputs.")
    print("Internal variables set to 0.0 are generally safe but check logic.")
    # We won't exit(1) to avoid blocking if only internal vars are 0.0
    sys.exit(0)
else:
    print("SUCCESS: No dangerous values found - safe to push")
    sys.exit(0)
