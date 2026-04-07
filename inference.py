import os
import json
import time
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN")   # NO default — intentional

import requests
from graders import get_grader
from tasks import get_task
from dataclasses import asdict

MAX_STEPS    = 30  # per task episode
TEMPERATURE  = 0.3

SYSTEM_PROMPT = """You are a quant trading agent. Each step you receive market observations and must respond with a JSON action.
Respond ONLY with valid JSON in this exact format:
{"action_type": "BUY" | "SELL" | "HOLD", "amount": <float>, "reasoning": "<string>"}
- BUY: spend this many USD to buy shares
- SELL: sell this many USD worth of shares  
- HOLD: amount must be 0.0
- Do not add any text outside the JSON."""

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error) -> None:
    error_val = error if error else "null"
    done_val  = str(done).lower()          # must be lowercase: true or false
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True
    )

def log_end(success: bool, steps: int, rewards: list) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True
    )

def main():
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )
    
    tasks = ["easy", "medium", "hard"]
    
    for task_name in tasks:
        success = False
        steps_taken = 0
        rewards = []
        episode_log = None
        
        log_start(task=task_name, env="qade", model=MODEL_NAME)
        
        try:
            resp = requests.post(f"http://localhost:7860/reset?task={task_name}")
            resp.raise_for_status()
            obs = resp.json()
            
            task_config_dict = asdict(get_task(task_name))
            episode_log = {
                "actions": [],
                "rewards": [],
                "portfolio_values": [obs.get("portfolio_value", 10000.0)],
                "final_portfolio_value": obs.get("portfolio_value", 10000.0),
                "initial_portfolio_value": obs.get("portfolio_value", 10000.0),
                "steps_taken": 0,
                "task_config": task_config_dict
            }
            
            done = False
            for step in range(1, MAX_STEPS + 1):
                if done:
                    break
                    
                error_str = None
                action_json = {"action_type": "HOLD", "amount": 0.0, "reasoning": "default initialization"}
                
                # OpenAI Call
                try:
                    obs_str = json.dumps(obs, indent=2)
                    completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"Observation:\n{obs_str}\nProvide your action."}
                        ],
                        temperature=TEMPERATURE,
                    )
                    raw_response = completion.choices[0].message.content or ""
                    action_str_raw = raw_response.strip()
                    
                    if action_str_raw.startswith("```json"): action_str_raw = action_str_raw[7:]
                    elif action_str_raw.startswith("```"): action_str_raw = action_str_raw[3:]
                    if action_str_raw.endswith("```"): action_str_raw = action_str_raw[:-3]
                    action_str_raw = action_str_raw.strip()
                    
                    action_json = json.loads(action_str_raw)
                    if "amount" not in action_json: action_json["amount"] = 0.0
                    if "action_type" not in action_json: action_json["action_type"] = "HOLD"

                except Exception as e:
                    error_str = f"LLMError: {str(e)}"
                    action_json = {"action_type": "HOLD", "amount": 0.0, "reasoning": "parse or API failure"}
                    
                # Format action string strictly adhering to constraint format: NO newlines
                action_str = json.dumps(action_json).replace("\n", " ").replace("\r", "")
                
                # Step ENV
                reward_val = 0.0
                try:
                    step_resp = requests.post(f"http://localhost:7860/step?task={task_name}", json=action_json)
                    step_resp.raise_for_status()
                    result = step_resp.json()
                    
                    obs = result.get("observation", obs)
                    reward_val = result.get("reward", 0.0)
                    done = result.get("done", False)
                    if "error" in result.get("info", {}):
                        error_str = error_str + f" | EnvError: {result['info']['error']}" if error_str else f"EnvError: {result['info']['error']}"
                except Exception as e:
                    error_str = error_str + f" | EnvError: {str(e)}" if error_str else f"EnvError: {str(e)}"
                    done = True
                    
                rewards.append(reward_val)
                steps_taken = step
                
                log_step(step=step, action=action_str, reward=reward_val, done=done, error=error_str)
                
                if episode_log is not None:
                    episode_log["portfolio_values"].append(obs.get("portfolio_value", 0.0))
                    episode_log["actions"].append(action_json)
                    episode_log["rewards"].append(reward_val)
                
                if done:
                    break
                    
            success = sum(rewards) > 0
            
        except Exception as e:
            error = str(e)
            print(f"Failed to reset or execute task {task_name}: {error}")
            
        finally:
            log_end(success=success, steps=steps_taken, rewards=rewards)
            
            if episode_log is not None and steps_taken > 0:
                episode_log["steps_taken"] = steps_taken
                episode_log["final_portfolio_value"] = episode_log["portfolio_values"][-1]
                
                grader_func = get_grader(task_name)
                score = grader_func(episode_log)
                
                print(f"Task Summary: {task_name} | Total Reward: {sum(rewards):.2f}")
                print(f"GRADER SCORE [{task_name}]: {score:.3f}\n")

if __name__ == "__main__":
    main()
