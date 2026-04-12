import subprocess, re, sys

FORBIDDEN = {0.0, 1.0}

def check_line(line: str, line_num: int) -> list:
    errors = []
    
    if line.startswith("[STEP]"):
        m = re.search(r'reward=(\d+\.\d+)', line)
        if m:
            r = float(m.group(1))
            if r == 0.0:
                errors.append(f"Line {line_num}: reward is exactly 0.0")
            if r == 1.0:
                errors.append(f"Line {line_num}: reward is exactly 1.0")
            if not (0.0 < r < 1.0):
                errors.append(f"Line {line_num}: reward {r} outside (0,1)")
    
    if line.startswith("[END]"):
        m = re.search(r'rewards=(.+)', line)
        if m:
            vals = m.group(1).split(",")
            unique = set(vals)
            # Check for too many identical values (fake env detection)
            if len(vals) > 5 and len(unique) < len(vals) * 0.3:
                errors.append(
                    f"Line {line_num}: rewards not varied enough "
                    f"({len(unique)} unique out of {len(vals)}) "
                    f"— validator may detect fake environment"
                )
            for v in vals:
                try:
                    r = float(v)
                    if r == 0.0 or r == 1.0:
                        errors.append(f"Line {line_num}: forbidden reward {r} in [END]")
                except ValueError:
                    errors.append(f"Line {line_num}: cannot parse reward {v!r}")
    
    return errors

# Test against sample output
sample_output = """
[START] task=bull_trend env=qade model=test
[STEP] step=1 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=2 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=3 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[END] success=true steps=3 rewards=0.050000,0.050000,0.050000
""".strip()

print("=== Verifying output ===\n")
all_errors = []
for i, line in enumerate(sample_output.split("\n"), 1):
    errs = check_line(line.strip(), i)
    all_errors.extend(errs)

if all_errors:
    print("❌ PROBLEMS FOUND:")
    for e in all_errors:
        print(f"  {e}")
    print("\nFix these before pushing!")
else:
    print("✅ Output looks clean")
