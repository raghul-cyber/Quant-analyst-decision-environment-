import re, math, sys

# ═══════════════════════════════════════
# ACTUAL full stdout output from REFINED run
# ═══════════════════════════════════════
ACTUAL_OUTPUT = """
[START] task=bull_trend env=qade model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=HOLD amt=0.00 reward=0.120000 done=false error=null
[STEP] step=2 action=HOLD amt=0.00 reward=0.120000 done=false error=null
[STEP] step=3 action=BUY amt=800.00 reward=0.099460 done=false error=null
[STEP] step=4 action=HOLD amt=0.00 reward=0.077697 done=false error=null
[STEP] step=5 action=SELL amt=237.43 reward=0.122804 done=false error=null
[STEP] step=6 action=BUY amt=800.00 reward=0.017037 done=false error=null
[STEP] step=7 action=SELL amt=402.59 reward=0.109830 done=false error=null
[STEP] step=8 action=SELL amt=188.27 reward=0.026073 done=false error=null
[STEP] step=9 action=SELL amt=221.50 reward=0.065564 done=false error=null
[STEP] step=10 action=SELL amt=152.99 reward=0.103528 done=false error=null
[STEP] step=11 action=HOLD amt=0.00 reward=0.133259 done=false error=null
[STEP] step=12 action=BUY amt=800.00 reward=0.259979 done=false error=null
[STEP] step=13 action=HOLD amt=0.00 reward=0.113256 done=false error=null
[STEP] step=14 action=HOLD amt=0.00 reward=0.102458 done=false error=null
[STEP] step=15 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=16 action=SELL amt=401.22 reward=0.066103 done=false error=null
[STEP] step=17 action=SELL amt=278.83 reward=0.084915 done=false error=null
[STEP] step=18 action=HOLD amt=0.00 reward=0.154469 done=false error=null
[STEP] step=19 action=BUY amt=800.00 reward=0.125146 done=false error=null
[STEP] step=20 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=21 action=SELL amt=489.06 reward=0.118653 done=false error=null
[STEP] step=22 action=HOLD amt=0.00 reward=0.097772 done=false error=null
[STEP] step=23 action=HOLD amt=0.00 reward=0.081060 done=false error=null
[STEP] step=24 action=SELL amt=339.81 reward=0.124483 done=false error=null
[STEP] step=25 action=BUY amt=800.00 reward=0.183116 done=false error=null
[STEP] step=26 action=BUY amt=800.00 reward=0.363254 done=false error=null
[STEP] step=27 action=BUY amt=800.00 reward=0.002000 done=false error=null
[STEP] step=28 action=SELL amt=600.00 reward=0.059335 done=false error=null
[STEP] step=29 action=HOLD amt=0.00 reward=0.163466 done=false error=null
[STEP] step=30 action=BUY amt=200.00 reward=0.238148 done=true error=null
[END] success=true steps=30 rewards=0.120000,0.120000,0.099460,0.077697,0.122804,0.017037,0.109830,0.026073,0.065564,0.103528,0.133259,0.259979,0.113256,0.102458,0.002000,0.066103,0.084915,0.154469,0.125146,0.002000,0.118653,0.097772,0.081060,0.124483,0.183116,0.363254,0.002000,0.059335,0.163466,0.238148
[START] task=noisy_market env=qade model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=HOLD amt=0.00 reward=0.120000 done=false error=null
[STEP] step=2 action=HOLD amt=0.00 reward=0.120000 done=false error=null
[STEP] step=3 action=BUY amt=800.00 reward=0.099460 done=false error=null
[STEP] step=4 action=HOLD amt=0.00 reward=0.077697 done=false error=null
[STEP] step=5 action=SELL amt=237.43 reward=0.122804 done=false error=null
[STEP] step=6 action=BUY amt=800.00 reward=0.017037 done=false error=null
[STEP] step=7 action=SELL amt=402.59 reward=0.109830 done=false error=null
[STEP] step=8 action=SELL amt=188.27 reward=0.026073 done=false error=null
[STEP] step=9 action=SELL amt=221.50 reward=0.065564 done=false error=null
[STEP] step=10 action=SELL amt=152.99 reward=0.103528 done=false error=null
[STEP] step=11 action=HOLD amt=0.00 reward=0.133259 done=false error=null
[STEP] step=12 action=BUY amt=800.00 reward=0.259979 done=false error=null
[STEP] step=13 action=HOLD amt=0.00 reward=0.113256 done=false error=null
[STEP] step=14 action=HOLD amt=0.00 reward=0.102458 done=false error=null
[STEP] step=15 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=16 action=SELL amt=401.22 reward=0.066103 done=false error=null
[STEP] step=17 action=SELL amt=278.83 reward=0.084915 done=false error=null
[STEP] step=18 action=HOLD amt=0.00 reward=0.154469 done=false error=null
[STEP] step=19 action=BUY amt=800.00 reward=0.125146 done=false error=null
[STEP] step=20 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=21 action=SELL amt=489.06 reward=0.118653 done=false error=null
[STEP] step=22 action=HOLD amt=0.00 reward=0.097772 done=false error=null
[STEP] step=23 action=HOLD amt=0.00 reward=0.081060 done=false error=null
[STEP] step=24 action=SELL amt=339.81 reward=0.124483 done=false error=null
[STEP] step=25 action=BUY amt=800.00 reward=0.183116 done=false error=null
[STEP] step=26 action=BUY amt=800.00 reward=0.363254 done=false error=null
[STEP] step=27 action=BUY amt=800.00 reward=0.002000 done=false error=null
[STEP] step=28 action=SELL amt=600.00 reward=0.059335 done=false error=null
[STEP] step=29 action=HOLD amt=0.00 reward=0.163466 done=false error=null
[STEP] step=30 action=BUY amt=200.00 reward=0.238148 done=false error=null
[STEP] step=31 action=BUY amt=800.00 reward=0.012405 done=false error=null
[STEP] step=32 action=SELL amt=400.00 reward=0.069903 done=false error=null
[STEP] step=33 action=HOLD amt=0.00 reward=0.002000 done=false error=null
[STEP] step=34 action=SELL amt=600.00 reward=0.002000 done=false error=null
[STEP] step=35 action=SELL amt=600.00 reward=0.180256 done=false error=null
[STEP] step=36 action=BUY amt=800.00 reward=0.289767 done=false error=null
[STEP] step=37 action=BUY amt=800.00 reward=0.086920 done=false error=null
[STEP] step=38 action=HOLD amt=0.00 reward=0.302193 done=false error=null
[STEP] step=39 action=BUY amt=800.00 reward=0.180617 done=false error=null
[STEP] step=40 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=41 action=SELL amt=600.00 reward=0.173146 done=false error=null
[STEP] step=42 action=HOLD amt=0.00 reward=0.431965 done=false error=null
[STEP] step=43 action=BUY amt=800.00 reward=0.091236 done=false error=null
[STEP] step=44 action=HOLD amt=0.00 reward=0.502705 done=false error=null
[STEP] step=45 action=BUY amt=800.00 reward=0.002000 done=false error=null
[STEP] step=46 action=SELL amt=600.00 reward=0.307732 done=false error=null
[STEP] step=47 action=BUY amt=800.00 reward=0.125581 done=false error=null
[STEP] step=48 action=SELL amt=400.00 reward=0.018091 done=false error=null
[STEP] step=49 action=HOLD amt=0.00 reward=0.145103 done=false error=null
[STEP] step=50 action=BUY amt=200.00 reward=0.002000 done=true error=null
[END] success=true steps=50 rewards=0.120000,0.120000,0.099460,0.077697,0.122804,0.017037,0.109830,0.026073,0.065564,0.103528,0.133259,0.259979,0.113256,0.102458,0.002000,0.066103,0.084915,0.154469,0.125146,0.002000,0.118653,0.097772,0.081060,0.124483,0.183116,0.363254,0.002000,0.059335,0.163466,0.238148,0.012405,0.069903,0.002000,0.002000,0.180256,0.289767,0.086920,0.302193,0.180617,0.002000,0.173146,0.431965,0.091236,0.502705,0.002000,0.307732,0.125581,0.018091,0.145103,0.002000
[START] task=shock_recovery env=qade model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=HOLD amt=0.00 reward=0.120000 done=false error=null
[STEP] step=2 action=HOLD amt=0.00 reward=0.120000 done=false error=null
[STEP] step=3 action=BUY amt=800.00 reward=0.099460 done=false error=null
[STEP] step=4 action=HOLD amt=0.00 reward=0.077697 done=false error=null
[STEP] step=5 action=SELL amt=237.43 reward=0.122804 done=false error=null
[STEP] step=6 action=BUY amt=800.00 reward=0.017037 done=false error=null
[STEP] step=7 action=SELL amt=402.59 reward=0.109830 done=false error=null
[STEP] step=8 action=SELL amt=188.27 reward=0.026073 done=false error=null
[STEP] step=9 action=SELL amt=221.50 reward=0.065564 done=false error=null
[STEP] step=10 action=SELL amt=152.99 reward=0.103528 done=false error=null
[STEP] step=11 action=HOLD amt=0.00 reward=0.133259 done=false error=null
[STEP] step=12 action=BUY amt=800.00 reward=0.259979 done=false error=null
[STEP] step=13 action=HOLD amt=0.00 reward=0.113256 done=false error=null
[STEP] step=14 action=HOLD amt=0.00 reward=0.102458 done=false error=null
[STEP] step=15 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=16 action=SELL amt=401.22 reward=0.066103 done=false error=null
[STEP] step=17 action=SELL amt=278.83 reward=0.084915 done=false error=null
[STEP] step=18 action=HOLD amt=0.00 reward=0.154469 done=false error=null
[STEP] step=19 action=BUY amt=800.00 reward=0.125146 done=false error=null
[STEP] step=20 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=21 action=SELL amt=489.06 reward=0.118653 done=false error=null
[STEP] step=22 action=HOLD amt=0.00 reward=0.097772 done=false error=null
[STEP] step=23 action=HOLD amt=0.00 reward=0.081060 done=false error=null
[STEP] step=24 action=SELL amt=339.81 reward=0.124483 done=false error=null
[STEP] step=25 action=BUY amt=800.00 reward=0.183116 done=false error=null
[STEP] step=26 action=BUY amt=800.00 reward=0.363254 done=false error=null
[STEP] step=27 action=BUY amt=800.00 reward=0.002000 done=false error=null
[STEP] step=28 action=SELL amt=600.00 reward=0.059335 done=false error=null
[STEP] step=29 action=HOLD amt=0.00 reward=0.163466 done=false error=null
[STEP] step=30 action=BUY amt=200.00 reward=0.238148 done=false error=null
[STEP] step=31 action=BUY amt=800.00 reward=0.012405 done=false error=null
[STEP] step=32 action=SELL amt=400.00 reward=0.069903 done=false error=null
[STEP] step=33 action=HOLD amt=0.00 reward=0.002000 done=false error=null
[STEP] step=34 action=SELL amt=600.00 reward=0.002000 done=false error=null
[STEP] step=35 action=SELL amt=600.00 reward=0.180256 done=false error=null
[STEP] step=36 action=BUY amt=800.00 reward=0.289767 done=false error=null
[STEP] step=37 action=BUY amt=800.00 reward=0.086920 done=false error=null
[STEP] step=38 action=HOLD amt=0.00 reward=0.302193 done=false error=null
[STEP] step=39 action=BUY amt=800.00 reward=0.180617 done=false error=null
[STEP] step=40 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=41 action=SELL amt=600.00 reward=0.173146 done=false error=null
[STEP] step=42 action=HOLD amt=0.00 reward=0.431965 done=false error=null
[STEP] step=43 action=BUY amt=800.00 reward=0.091236 done=false error=null
[STEP] step=44 action=HOLD amt=0.00 reward=0.502705 done=false error=null
[STEP] step=45 action=BUY amt=800.00 reward=0.002000 done=false error=null
[STEP] step=46 action=SELL amt=600.00 reward=0.307732 done=false error=null
[STEP] step=47 action=BUY amt=800.00 reward=0.125581 done=false error=null
[STEP] step=48 action=SELL amt=400.00 reward=0.018091 done=false error=null
[STEP] step=49 action=HOLD amt=0.00 reward=0.145103 done=false error=null
[STEP] step=50 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=51 action=SELL amt=600.00 reward=0.044906 done=false error=null
[STEP] step=52 action=HOLD amt=0.00 reward=0.209467 done=false error=null
[STEP] step=53 action=HOLD amt=0.00 reward=0.490913 done=false error=null
[STEP] step=54 action=BUY amt=800.00 reward=0.002000 done=false error=null
[STEP] step=55 action=SELL amt=600.00 reward=0.002000 done=false error=null
[STEP] step=56 action=SELL amt=600.00 reward=0.002000 done=false error=null
[STEP] step=57 action=SELL amt=600.00 reward=0.282722 done=false error=null
[STEP] step=58 action=BUY amt=800.00 reward=0.179296 done=false error=null
[STEP] step=59 action=HOLD amt=0.00 reward=0.002000 done=false error=null
[STEP] step=60 action=SELL amt=600.00 reward=0.208066 done=false error=null
[STEP] step=61 action=BUY amt=800.00 reward=0.124427 done=false error=null
[STEP] step=62 action=HOLD amt=0.00 reward=0.513851 done=false error=null
[STEP] step=63 action=BUY amt=800.00 reward=0.002000 done=false error=null
[STEP] step=64 action=SELL amt=600.00 reward=0.014143 done=false error=null
[STEP] step=65 action=BUY amt=200.00 reward=0.002000 done=false error=null
[STEP] step=66 action=HOLD amt=0.00 reward=0.002000 done=false error=null
[STEP] step=67 action=SELL amt=600.00 reward=0.170701 done=false error=null
[STEP] step=68 action=HOLD amt=0.00 reward=0.182425 done=false error=null
[STEP] step=69 action=HOLD amt=0.00 reward=0.271224 done=false error=null
[STEP] step=70 action=BUY amt=200.00 reward=0.041435 done=false error=null
[STEP] step=71 action=HOLD amt=0.00 reward=0.002000 done=false error=null
[STEP] step=72 action=SELL amt=600.00 reward=0.008829 done=false error=null
[STEP] step=73 action=HOLD amt=0.00 reward=0.045897 done=false error=null
[STEP] step=74 action=HOLD amt=0.00 reward=0.002000 done=false error=null
[STEP] step=75 action=SELL amt=600.00 reward=0.070361 done=false error=null
[STEP] step=76 action=HOLD amt=0.00 reward=0.194176 done=false error=null
[STEP] step=77 action=HOLD amt=0.00 reward=0.467153 done=false error=null
[STEP] step=78 action=BUY amt=800.00 reward=0.289682 done=false error=null
[STEP] step=79 action=HOLD amt=0.00 reward=0.378597 done=false error=null
[STEP] step=80 action=BUY amt=200.00 reward=0.082276 done=true error=null
[END] success=true steps=80 rewards=0.120000,0.120000,0.099460,0.077697,0.122804,0.017037,0.109830,0.026073,0.065564,0.103528,0.133259,0.259979,0.113256,0.102458,0.002000,0.066103,0.084915,0.154469,0.125146,0.002000,0.118653,0.097772,0.081060,0.124483,0.183116,0.363254,0.002000,0.059335,0.163466,0.238148,0.012405,0.069903,0.002000,0.002000,0.180256,0.289767,0.086920,0.302193,0.180617,0.002000,0.173146,0.431965,0.091236,0.502705,0.002000,0.307732,0.125581,0.018091,0.145103,0.002000,0.044906,0.209467,0.490913,0.002000,0.002000,0.002000,0.282722,0.179296,0.002000,0.208066,0.124427,0.513851,0.002000,0.014143,0.002000,0.002000,0.170701,0.182425,0.271224,0.041435,0.002000,0.008829,0.045897,0.002000,0.070361,0.194176,0.467153,0.289682,0.378597,0.082276
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
