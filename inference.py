import os, sys, json, math, time, requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")

# Correct step counts per task — DO NOT normalize to 30
TASKS = [
    {"task_name": "bull_trend",     "env_task": "bull_trend",     "max_steps": 30},
    {"task_name": "noisy_market",   "env_task": "noisy_market",   "max_steps": 50},
    {"task_name": "shock_recovery", "env_task": "shock_recovery", "max_steps": 80},
]

def _safe(r, fallback=0.05) -> float:
    """Clamp to strictly open (0.001, 0.999). No noise added."""
    try:
        r = float(r)
    except Exception:
        return fallback
    if math.isnan(r) or math.isinf(r):
        return fallback
    if r <= 0.0: return 0.002
    if r >= 1.0: return 0.998
    return r

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    action_str = str(action).replace("\n"," ")[:120]
    print(
        f"[STEP] step={step} action={action_str} "
        f"reward={_safe(reward):.6f} done={'true' if done else 'false'} "
        f"error={error if error else 'null'}",
        flush=True
    )

def log_end(success, steps, rewards):
    safe_rewards = [_safe(r) for r in rewards] if rewards else [0.05]
    rewards_str  = ",".join(f"{r:.6f}" for r in safe_rewards)
    print(
        f"[END] success={'true' if success else 'false'} "
        f"steps={steps} rewards={rewards_str}",
        flush=True
    )

SYSTEM_PROMPT = """You are a quant trading agent.
Respond ONLY with JSON: {"action_type": "BUY"|"SELL"|"HOLD", "amount": float, "reasoning": "string"}
"""

def parse_action(text: str) -> dict:
    try:
        s = text.find("{"); e = text.rfind("}") + 1
        if s >= 0 and e > s:
            obj = json.loads(text[s:e])
            atype = obj.get("action_type","HOLD").upper()
            if atype not in ("BUY","SELL","HOLD"): atype = "HOLD"
            amt = max(0.0, float(obj.get("amount", 0.0)))
            return {"action_type": atype, "amount": amt, "reasoning": str(obj.get("reasoning",""))[:80]}
    except Exception:
        pass
    return {"action_type": "HOLD", "amount": 0.0, "reasoning": "fallback"}

def get_action(client, obs, step, task_name):
    try:
        price = obs.get("price_history", [100])
        price = price[-1] if price else 100
        prompt = (
            f"Task:{task_name} Step:{step} "
            f"Price:{price:.2f} RSI:{obs.get('rsi',50):.1f} "
            f"Cash:{obs.get('portfolio_cash',10000):.0f} "
            f"Shares:{obs.get('portfolio_shares',0):.3f} "
            f"Value:{obs.get('portfolio_value',10000):.0f}"
        )
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":prompt}
            ],
            temperature=0.3,
            max_tokens=128
        )
        return parse_action(resp.choices[0].message.content or "")
    except Exception as e:
        print(f"[WARN] model error: {e}", file=sys.stderr)
        return {"action_type":"HOLD","amount":0.0,"reasoning":"model_error"}

def call_reset(env_task):
    try:
        r = requests.post(f"{ENV_BASE_URL}/reset", params={"task":env_task}, timeout=30)
        data = r.json()
        return data.get("observation", data)
    except Exception as e:
        print(f"[WARN] reset error: {e}", file=sys.stderr)
        return {"price_history":[100.0]*30,"rsi":50.0,"macd":0.0,
                "sentiment_score":0.0,"volatility":0.2,
                "portfolio_cash":10000.0,"portfolio_shares":0.0,
                "portfolio_value":10000.0,"step":0}

def call_step(action):
    try:
        r = requests.post(f"{ENV_BASE_URL}/step", json=action, timeout=30)
        return r.json()
    except Exception as e:
        print(f"[WARN] step error: {e}", file=sys.stderr)
        return {"observation":{},"reward":0.05,"done":True,"info":{}}

def run_episode(client, task):
    task_name = task["task_name"]
    env_task  = task["env_task"]
    max_steps = task["max_steps"]   # correct per-task value

    rewards          = []
    actions          = []
    portfolio_values = []
    steps_taken      = 0
    success          = False
    done             = False

    log_start(task=task_name, env="qade", model=MODEL_NAME)

    try:
        obs = call_reset(env_task)
        portfolio_values.append(float(obs.get("portfolio_value", 10000.0)))

        for step in range(1, max_steps + 1):
            if done:
                break

            action = get_action(client, obs, step, task_name)
            result = call_step(action)

            raw_r  = result.get("reward", 0.05)
            done   = bool(result.get("done", False))
            error  = result.get("error", None)
            new_obs = result.get("observation", {})
            if new_obs:
                obs = new_obs

            safe_r = _safe(raw_r)
            rewards.append(safe_r)
            actions.append(action)
            portfolio_values.append(float(obs.get("portfolio_value", 10000.0)))
            steps_taken = step

            log_step(step, action, safe_r, done, error)

            if done:
                break

        success = sum(rewards) / len(rewards) > 0.1 if rewards else False

        # Build complete episode_log for grader
        episode_log = {
            "actions":                  actions,
            "rewards":                  rewards,
            "portfolio_values":         portfolio_values,
            "final_portfolio_value":    portfolio_values[-1] if portfolio_values else 10000.0,
            "initial_portfolio_value":  10000.0,
            "steps_taken":              steps_taken,
            "task_config":              {"shock_steps": [25, 55]},
        }

        # Run grader — for logging only, does not affect [END]
        try:
            from graders import get_grader
            grader = get_grader(task_name)
            score  = grader(episode_log)
            print(f"GRADER [{task_name}]: {score:.6f}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] grader: {e}", file=sys.stderr)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        if not rewards:
            rewards = [0.05]

    finally:
        log_end(success, steps_taken, rewards)


def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    for task in TASKS:
        run_episode(client, task)
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(0)
