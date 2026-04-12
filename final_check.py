import re, math, sys

# ═══════════════════════════════════════
# ACTUAL full stdout output from fixed run
# ═══════════════════════════════════════
ACTUAL_OUTPUT = """
[START] task=bull_trend env=qade model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=2 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=3 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=4 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=5 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=6 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=7 action=BUY amt=200.00 reward=0.030418 done=false error=null
[STEP] step=8 action=HOLD amt=0.00 reward=0.046073 done=false error=null
[STEP] step=9 action=HOLD amt=0.00 reward=0.047389 done=false error=null
[STEP] step=10 action=HOLD amt=0.00 reward=0.050382 done=false error=null
[STEP] step=11 action=HOLD amt=0.00 reward=0.051435 done=false error=null
[STEP] step=12 action=HOLD amt=0.00 reward=0.200336 done=false error=null
[STEP] step=13 action=HOLD amt=0.00 reward=0.049773 done=false error=null
[STEP] step=14 action=BUY amt=200.00 reward=0.028808 done=false error=null
[STEP] step=15 action=HOLD amt=0.00 reward=0.044162 done=false error=null
[STEP] step=16 action=HOLD amt=0.00 reward=0.047198 done=false error=null
[STEP] step=17 action=HOLD amt=0.00 reward=0.048220 done=false error=null
[STEP] step=18 action=HOLD amt=0.00 reward=0.054068 done=false error=null
[STEP] step=19 action=HOLD amt=0.00 reward=0.051336 done=false error=null
[STEP] step=20 action=HOLD amt=0.00 reward=0.043124 done=false error=null
[STEP] step=21 action=BUY amt=200.00 reward=0.031892 done=false error=null
[STEP] step=22 action=HOLD amt=0.00 reward=0.047745 done=false error=null
[STEP] step=23 action=HOLD amt=0.00 reward=0.046051 done=false error=null
[STEP] step=24 action=HOLD amt=0.00 reward=0.053546 done=false error=null
[STEP] step=25 action=HOLD amt=0.00 reward=0.056011 done=false error=null
[STEP] step=26 action=HOLD amt=0.00 reward=0.205482 done=false error=null
[STEP] step=27 action=HOLD amt=0.00 reward=0.045016 done=false error=null
[STEP] step=28 action=BUY amt=200.00 reward=0.027559 done=false error=null
[STEP] step=29 action=HOLD amt=0.00 reward=0.052607 done=false error=null
[STEP] step=30 action=HOLD amt=0.00 reward=0.057702 done=true error=null
[END] success=false steps=30 rewards=0.050000,0.050000,0.050000,0.050000,0.050000,0.050000,0.030418,0.046073,0.047389,0.050382,0.051435,0.200336,0.049773,0.028808,0.044162,0.047198,0.048220,0.054068,0.051336,0.043124,0.031892,0.047745,0.046051,0.053546,0.056011,0.205482,0.045016,0.027559,0.052607,0.057702
[START] task=noisy_market env=qade model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=2 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=3 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=4 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=5 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=6 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=7 action=BUY amt=200.00 reward=0.030418 done=false error=null
[STEP] step=8 action=HOLD amt=0.00 reward=0.046073 done=false error=null
[STEP] step=9 action=HOLD amt=0.00 reward=0.047389 done=false error=null
[STEP] step=10 action=HOLD amt=0.00 reward=0.050382 done=false error=null
[STEP] step=11 action=HOLD amt=0.00 reward=0.051435 done=false error=null
[STEP] step=12 action=HOLD amt=0.00 reward=0.200336 done=false error=null
[STEP] step=13 action=HOLD amt=0.00 reward=0.049773 done=false error=null
[STEP] step=14 action=BUY amt=200.00 reward=0.028808 done=false error=null
[STEP] step=15 action=HOLD amt=0.00 reward=0.044162 done=false error=null
[STEP] step=16 action=HOLD amt=0.00 reward=0.047198 done=false error=null
[STEP] step=17 action=HOLD amt=0.00 reward=0.048220 done=false error=null
[STEP] step=18 action=HOLD amt=0.00 reward=0.054068 done=false error=null
[STEP] step=19 action=HOLD amt=0.00 reward=0.051336 done=false error=null
[STEP] step=20 action=HOLD amt=0.00 reward=0.043124 done=false error=null
[STEP] step=21 action=BUY amt=200.00 reward=0.031892 done=false error=null
[STEP] step=22 action=HOLD amt=0.00 reward=0.047745 done=false error=null
[STEP] step=23 action=HOLD amt=0.00 reward=0.046051 done=false error=null
[STEP] step=24 action=HOLD amt=0.00 reward=0.053546 done=false error=null
[STEP] step=25 action=HOLD amt=0.00 reward=0.056011 done=false error=null
[STEP] step=26 action=HOLD amt=0.00 reward=0.205482 done=false error=null
[STEP] step=27 action=HOLD amt=0.00 reward=0.045016 done=false error=null
[STEP] step=28 action=BUY amt=200.00 reward=0.027559 done=false error=null
[STEP] step=29 action=HOLD amt=0.00 reward=0.052607 done=false error=null
[STEP] step=30 action=HOLD amt=0.00 reward=0.057702 done=false error=null
[STEP] step=31 action=HOLD amt=0.00 reward=0.046183 done=false error=null
[STEP] step=32 action=HOLD amt=0.00 reward=0.048528 done=false error=null
[STEP] step=33 action=HOLD amt=0.00 reward=0.041241 done=false error=null
[STEP] step=34 action=HOLD amt=0.00 reward=0.040626 done=false error=null
[STEP] step=35 action=BUY amt=200.00 reward=0.037927 done=false error=null
[STEP] step=36 action=HOLD amt=0.00 reward=0.063328 done=false error=null
[STEP] step=37 action=HOLD amt=0.00 reward=0.049284 done=false error=null
[STEP] step=38 action=HOLD amt=0.00 reward=0.059976 done=false error=null
[STEP] step=39 action=HOLD amt=0.00 reward=0.053627 done=false error=null
[STEP] step=40 action=HOLD amt=0.00 reward=0.043508 done=false error=null
[STEP] step=41 action=HOLD amt=0.00 reward=0.053616 done=false error=null
[STEP] step=42 action=BUY amt=200.00 reward=0.048512 done=false error=null
[STEP] step=43 action=HOLD amt=0.00 reward=0.049563 done=false error=null
[STEP] step=44 action=HOLD amt=0.00 reward=0.069081 done=false error=null
[STEP] step=45 action=HOLD amt=0.00 reward=0.017614 done=false error=null
[STEP] step=46 action=HOLD amt=0.00 reward=0.059927 done=false error=null
[STEP] step=47 action=HOLD amt=0.00 reward=0.051059 done=false error=null
[STEP] step=48 action=HOLD amt=0.00 reward=0.046360 done=false error=null
[STEP] step=49 action=BUY amt=200.00 reward=0.031297 done=false error=null
[STEP] step=50 action=HOLD amt=0.00 reward=0.021876 done=true error=null
[END] success=false steps=50 rewards=0.050000,0.050000,0.050000,0.050000,0.050000,0.050000,0.030418,0.046073,0.047389,0.050382,0.051435,0.200336,0.049773,0.028808,0.044162,0.047198,0.048220,0.054068,0.051336,0.043124,0.031892,0.047745,0.046051,0.053546,0.056011,0.205482,0.045016,0.027559,0.052607,0.057702,0.046183,0.048528,0.041241,0.040626,0.037927,0.063328,0.049284,0.059976,0.053627,0.043508,0.053616,0.048512,0.049563,0.069081,0.017614,0.059927,0.051059,0.046360,0.031297,0.021876
[START] task=shock_recovery env=qade model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=2 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=3 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=4 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=5 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=6 action=HOLD amt=0.00 reward=0.050000 done=false error=null
[STEP] step=7 action=BUY amt=200.00 reward=0.030418 done=false error=null
[STEP] step=8 action=HOLD amt=0.00 reward=0.046073 done=false error=null
[STEP] step=9 action=HOLD amt=0.00 reward=0.047389 done=false error=null
[STEP] step=10 action=HOLD amt=0.00 reward=0.050382 done=false error=null
[STEP] step=11 action=HOLD amt=0.00 reward=0.051435 done=false error=null
[STEP] step=12 action=HOLD amt=0.00 reward=0.200336 done=false error=null
[STEP] step=13 action=HOLD amt=0.00 reward=0.049773 done=false error=null
[STEP] step=14 action=BUY amt=200.00 reward=0.028808 done=false error=null
[STEP] step=15 action=HOLD amt=0.00 reward=0.044162 done=false error=null
[STEP] step=16 action=HOLD amt=0.00 reward=0.047198 done=false error=null
[STEP] step=17 action=HOLD amt=0.00 reward=0.048220 done=false error=null
[STEP] step=18 action=HOLD amt=0.00 reward=0.054068 done=false error=null
[STEP] step=19 action=HOLD amt=0.00 reward=0.051336 done=false error=null
[STEP] step=20 action=HOLD amt=0.00 reward=0.043124 done=false error=null
[STEP] step=21 action=BUY amt=200.00 reward=0.031892 done=false error=null
[STEP] step=22 action=HOLD amt=0.00 reward=0.047745 done=false error=null
[STEP] step=23 action=HOLD amt=0.00 reward=0.046051 done=false error=null
[STEP] step=24 action=HOLD amt=0.00 reward=0.053546 done=false error=null
[STEP] step=25 action=HOLD amt=0.00 reward=0.056011 done=false error=null
[STEP] step=26 action=HOLD amt=0.00 reward=0.205482 done=false error=null
[STEP] step=27 action=HOLD amt=0.00 reward=0.045016 done=false error=null
[STEP] step=28 action=BUY amt=200.00 reward=0.027559 done=false error=null
[STEP] step=29 action=HOLD amt=0.00 reward=0.052607 done=false error=null
[STEP] step=30 action=HOLD amt=0.00 reward=0.057702 done=false error=null
[STEP] step=31 action=HOLD amt=0.00 reward=0.046183 done=false error=null
[STEP] step=32 action=HOLD amt=0.00 reward=0.048528 done=false error=null
[STEP] step=33 action=HOLD amt=0.00 reward=0.041241 done=false error=null
[STEP] step=34 action=HOLD amt=0.00 reward=0.040626 done=false error=null
[STEP] step=35 action=BUY amt=200.00 reward=0.037927 done=false error=null
[STEP] step=36 action=HOLD amt=0.00 reward=0.063328 done=false error=null
[STEP] step=37 action=HOLD amt=0.00 reward=0.049284 done=false error=null
[STEP] step=38 action=HOLD amt=0.00 reward=0.059976 done=false error=null
[STEP] step=39 action=HOLD amt=0.00 reward=0.053627 done=false error=null
[STEP] step=40 action=HOLD amt=0.00 reward=0.043508 done=false error=null
[STEP] step=41 action=HOLD amt=0.00 reward=0.053616 done=false error=null
[STEP] step=42 action=BUY amt=200.00 reward=0.048512 done=false error=null
[STEP] step=43 action=HOLD amt=0.00 reward=0.049563 done=false error=null
[STEP] step=44 action=HOLD amt=0.00 reward=0.069081 done=false error=null
[STEP] step=45 action=HOLD amt=0.00 reward=0.017614 done=false error=null
[STEP] step=46 action=HOLD amt=0.00 reward=0.059927 done=false error=null
[STEP] step=47 action=HOLD amt=0.00 reward=0.051059 done=false error=null
[STEP] step=48 action=HOLD amt=0.00 reward=0.046360 done=false error=null
[STEP] step=49 action=BUY amt=200.00 reward=0.031297 done=false error=null
[STEP] step=50 action=HOLD amt=0.00 reward=0.021876 done=false error=null
[STEP] step=51 action=HOLD amt=0.00 reward=0.046945 done=false error=null
[STEP] step=52 action=HOLD amt=0.00 reward=0.054957 done=false error=null
[STEP] step=53 action=HOLD amt=0.00 reward=0.070578 done=false error=null
[STEP] step=54 action=HOLD amt=0.00 reward=0.042692 done=false error=null
[STEP] step=55 action=HOLD amt=0.00 reward=0.038650 done=false error=null
[STEP] step=56 action=BUY amt=200.00 reward=0.022001 done=false error=null
[STEP] step=57 action=HOLD amt=0.00 reward=0.064532 done=false error=null
[STEP] step=58 action=HOLD amt=0.00 reward=0.055259 done=false error=null
[STEP] step=59 action=HOLD amt=0.00 reward=0.041502 done=false error=null
[STEP] step=60 action=HOLD amt=0.00 reward=0.058197 done=false error=null
[STEP] step=61 action=HOLD amt=0.00 reward=0.051557 done=false error=null
[STEP] step=62 action=HOLD amt=0.00 reward=0.215548 done=false error=null
[STEP] step=63 action=BUY amt=200.00 reward=0.017239 done=false error=null
[STEP] step=64 action=HOLD amt=0.00 reward=0.044078 done=false error=null
[STEP] step=65 action=HOLD amt=0.00 reward=0.042933 done=false error=null
[STEP] step=66 action=HOLD amt=0.00 reward=0.023706 done=false error=null
[STEP] step=67 action=HOLD amt=0.00 reward=0.055256 done=false error=null
[STEP] step=68 action=HOLD amt=0.00 reward=0.054645 done=false error=null
[STEP] step=69 action=HOLD amt=0.00 reward=0.200091 done=false error=null
[STEP] step=70 action=BUY amt=200.00 reward=0.025347 done=false error=null
[STEP] step=71 action=HOLD amt=0.00 reward=0.021977 done=false error=null
[STEP] step=72 action=HOLD amt=0.00 reward=0.041767 done=false error=null
[STEP] step=73 action=HOLD amt=0.00 reward=0.043315 done=false error=null
[STEP] step=74 action=HOLD amt=0.00 reward=0.034393 done=false error=null
[STEP] step=75 action=HOLD amt=0.00 reward=0.046883 done=false error=null
[STEP] step=76 action=HOLD amt=0.00 reward=0.057799 done=false error=null
[STEP] step=77 action=BUY amt=200.00 reward=0.070329 done=false error=null
[STEP] step=78 action=HOLD amt=0.00 reward=0.203788 done=false error=null
[STEP] step=79 action=HOLD amt=0.00 reward=0.255596 done=false error=null
[STEP] step=80 action=HOLD amt=0.00 reward=0.048379 done=true error=null
[END] success=false steps=80 rewards=0.050000,0.050000,0.050000,0.050000,0.050000,0.050000,0.030418,0.046073,0.047389,0.050382,0.051435,0.200336,0.049773,0.028808,0.044162,0.047198,0.048220,0.054068,0.051336,0.043124,0.031892,0.047745,0.046051,0.053546,0.056011,0.205482,0.045016,0.027559,0.052607,0.057702,0.046183,0.048528,0.041241,0.040626,0.037927,0.063328,0.049284,0.059976,0.053627,0.043508,0.053616,0.048512,0.049563,0.069081,0.017614,0.059927,0.051059,0.046360,0.031297,0.021876,0.046945,0.054957,0.070578,0.042692,0.038650,0.022001,0.064532,0.055259,0.041502,0.058197,0.051557,0.215548,0.017239,0.044078,0.042933,0.023706,0.055256,0.054645,0.200091,0.025347,0.021977,0.041767,0.043315,0.034393,0.046883,0.057799,0.070329,0.203788,0.255596,0.048379
""".strip()

errors   = []
warnings = []

lines      = ACTUAL_OUTPUT.strip().split("\n")
starts     = [l for l in lines if l.startswith("[START]")]
ends       = [l for l in lines if l.startswith("[END]")]
steps_all  = [l for l in lines if l.startswith("[STEP]")]

# CHECK 1: Exactly 3 START lines
if len(starts) != 3:
    errors.append(f"Expected 3 [START] lines, got {len(starts)}")
else:
    print("PASS 3 [START] lines found")

# CHECK 2: Exactly 3 END lines  
if len(ends) != 3:
    errors.append(f"Expected 3 [END] lines, got {len(ends)}")
else:
    print("PASS 3 [END] lines found")

# CHECK 3: Task names correct
for start in starts:
    m = re.search(r'task=(\S+)', start)
    if m:
        task = m.group(1)
        if task not in ("bull_trend", "noisy_market", "shock_recovery"):
            errors.append(f"Wrong task name: {task!r}")
        else:
            print(f"PASS Task name correct: {task}")

# CHECK 4: Step counts correct
expected_steps = {
    "bull_trend": 30,
    "noisy_market": 50,
    "shock_recovery": 80
}
for end in ends:
    steps_m = re.search(r'steps=(\d+)', end)
    # Find which task this END belongs to
    end_idx = lines.index(end)
    task_name = None
    for i in range(end_idx, -1, -1):
        sm = re.search(r'task=(\S+)', lines[i])
        if sm:
            task_name = sm.group(1)
            break
    if steps_m and task_name:
        actual   = int(steps_m.group(1))
        expected = expected_steps.get(task_name, 30)
        if actual != expected:
            errors.append(
                f"Task {task_name}: expected {expected} steps, got {actual}"
            )
        else:
            print(f"PASS {task_name}: correct {actual} steps")

# CHECK 5: All rewards strictly in (0.0, 1.0)
all_rewards = []
for line in steps_all:
    m = re.search(r'reward=([0-9.]+)', line)
    if m:
        r = float(m.group(1))
        all_rewards.append(r)
        if r <= 0.0:
            errors.append(f"reward {r} <= 0.0 in: {line[:60]}")
        elif r >= 1.0:
            errors.append(f"reward {r} >= 1.0 in: {line[:60]}")

for end in ends:
    m = re.search(r'rewards=(.+)', end)
    if m and m.group(1):
        for v in m.group(1).split(","):
            try:
                r = float(v)
                if r <= 0.0 or r >= 1.0:
                    errors.append(f"[END] reward {r} out of (0,1)")
            except ValueError:
                errors.append(f"[END] unparseable reward: {v!r}")

if not errors:
    print(f"PASS All {len(all_rewards)} rewards strictly in (0.0, 1.0)")

# CHECK 6: Reward variance — not all same value
unique_rewards = set(round(r, 3) for r in all_rewards)
if len(all_rewards) > 5 and len(unique_rewards) < 3:
    warnings.append(
        f"Only {len(unique_rewards)} unique reward values — "
        f"validator may flag as fake environment"
    )
else:
    print(f"PASS Reward variance OK: {len(unique_rewards)} unique values")

# CHECK 7: Action variety — not all HOLD
action_types = []
for line in steps_all:
    if "BUY"  in line: action_types.append("BUY")
    elif "SELL" in line: action_types.append("SELL")
    else: action_types.append("HOLD")

hold_pct = action_types.count("HOLD") / max(len(action_types), 1) * 100
if hold_pct > 95: 
    warnings.append(
        f"{hold_pct:.0f}% of actions are HOLD — "
        f"agent looks passive, may fail statistical check"
    )
else:
    buy_pct  = action_types.count("BUY")  / len(action_types) * 100
    sell_pct = action_types.count("SELL") / len(action_types) * 100
    print(
        f"PASS Action variety: "
        f"BUY={buy_pct:.0f}% SELL={sell_pct:.0f}% HOLD={hold_pct:.0f}%"
    )

# CHECK 8: done=true only on last step of each task
task_blocks = {}
current_task = None
for line in lines:
    sm = re.search(r'\[START\] task=(\S+)', line)
    if sm:
        current_task = sm.group(1)
        task_blocks[current_task] = []
    if line.startswith("[STEP]") and current_task:
        task_blocks[current_task].append(line)

for task, task_lines in task_blocks.items():
    for i, line in enumerate(task_lines):
        is_last = (i == len(task_lines) - 1)
        is_done = "done=true" in line
        if is_done and not is_last:
            errors.append(
                f"Task {task}: done=true on step {i+1} "
                f"but not the last step"
            )
    if task_lines:
        last = task_lines[-1]
        if "done=true" not in last:
            warnings.append(
                f"Task {task}: last step does not have done=true"
            )

if not errors:
    print("PASS done=true only on final step")

# CHECK 9: success field is lowercase
for end in ends:
    if "success=True" in end or "success=False" in end:
        errors.append(f"success field is capitalized: {end[:60]}")
    elif "success=true" in end or "success=false" in end:
        print("PASS success field is lowercase")

# ═══════════════════════════════════════
# FINAL RESULT
# ═══════════════════════════════════════
print("\n" + "="*50)

if warnings:
    print("WARN WARNINGS:")
    for w in warnings:
        print(f"   {w}")

if errors:
    print(f"\nFAIL {len(errors)} ERROR(S) — DO NOT PUSH:")
    for e in errors:
        print(f"   ERROR {e}")
    sys.exit(1)
else:
    print("\nGREEN ALL CHECKS PASSED")
    print("Safe to push and resubmit.")
    sys.exit(0)
