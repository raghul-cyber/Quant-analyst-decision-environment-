import os
import sys

def print_pass(msg):
    print(f"✅ PASS: {msg}")

def print_fail(msg):
    print(f"❌ FAIL: {msg}")

def main():
    failures = 0
    print("Starting QADE Validation...\n")

    # 1. CHECK: Dockerfile
    if os.path.exists("Dockerfile"):
        try:
            with open("Dockerfile", "r", encoding="utf-8") as df:
                content = df.read()
                if "FROM" in content and "EXPOSE 7860" in content and "CMD" in content:
                    print_pass("Dockerfile contain FROM, EXPOSE 7860, and CMD")
                else:
                    print_fail("Dockerfile missing required directives")
                    failures += 1
        except Exception as e:
            print_fail(f"could not read Dockerfile: {e}")
            failures += 1
    else:
        print_fail("missing file Dockerfile")
        failures += 1

    # 2. CHECK: Required files exist
    required_files = [
        "env.py", "models.py", "reward.py", "inference.py", "openenv.yaml", 
        "README.md", "Dockerfile", "requirements.txt",
        os.path.join("tasks", "easy.py"), os.path.join("tasks", "medium.py"), os.path.join("tasks", "hard.py"),
        os.path.join("graders", "easy_grader.py"), os.path.join("graders", "medium_grader.py"), os.path.join("graders", "hard_grader.py")
    ]
    
    missing_files = []
    for f in required_files:
        if not os.path.exists(f):
            missing_files.append(f)
            
    if missing_files:
        for f in missing_files:
            print_fail(f"missing file {f.replace(os.sep, '/')}")
            failures += 1
    else:
        print_pass("all required files exist")


    # 3. CHECK: Import logic
    try:
        from models import QADEObservation, QADEAction, QADEReward, StepResult
        from reward import RewardCalculator
        from tasks import get_task
        from graders import get_grader
        print_pass("models import cleanly")
    except Exception as e:
        print_fail(f"Python module import error: {e}")
        failures += 1

    # 4. CHECK: Env Smoke test
    try:
        from env import QADEEnv
        env = QADEEnv("easy")
        obs = env.reset()
        
        from models import QADEObservation, QADEAction, StepResult
        if not isinstance(obs, QADEObservation):
            print_fail("reset() did not return QADEObservation")
            failures += 1
        else:
            action = QADEAction(action_type="BUY", amount=500.0, reasoning="test")
            result = env.step(action)
            if not isinstance(result, StepResult):
                print_fail("step() did not return StepResult")
                failures += 1
            else:
                if not isinstance(result.reward, float) or not isinstance(result.done, bool):
                    print_fail("StepResult reward not float or done not bool")
                    failures += 1
                else:
                    print_pass("Environment smoke test ran successfully")
    except Exception as e:
        print_fail(f"Environment smoke test exception: {e}")
        failures += 1

    # 5. CHECK: Graders
    try:
        from graders import get_grader
        episode_log = {
            "actions": [{"action_type": "BUY", "amount": 500.0}, {"action_type": "SELL", "amount": 500.0}],
            "rewards": [1.0, 2.0],
            "portfolio_values": [10000.0, 10500.0, 11000.0],
            "final_portfolio_value": 11000.0,
            "initial_portfolio_value": 10000.0,
            "steps_taken": 2,
            "task_config": {"price_params": {"shock_steps": []}}
        }
        grader_failures = 0
        for t in ["easy", "medium", "hard"]:
            fn = get_grader(t)
            score = fn(episode_log)
            if not isinstance(score, float) or score < 0.0 or score > 1.0:
                print_fail(f"{t} grader returned invalid score: {score}")
                grader_failures += 1
        if grader_failures == 0:
            print_pass("All 3 graders ran without error and returned valid floats")
        else:
            failures += grader_failures
    except Exception as e:
        print_fail(f"Grader execution exception: {e}")
        failures += 1


    # 6. CHECK: openenv.yaml
    if os.path.exists("openenv.yaml"):
        try:
            import yaml
            with open("openenv.yaml", "r", encoding="utf-8") as yf:
                yml_data = yaml.safe_load(yf)
                req_keys = ["name", "version", "tasks", "observation_space", "action_space", "endpoints"]
                missing = [k for k in req_keys if k not in yml_data]
                if missing:
                    print_fail(f"openenv.yaml missing keys: {missing}")
                    failures += 1
                else:
                    print_pass("openenv.yaml is valid YAML and has required keys")
        except ImportError:
            print_fail("PyYAML not installed to check openenv.yaml (please pip install pyyaml)")
            failures += 1
        except Exception as e:
            print_fail(f"openenv.yaml parsing error: {e}")
            failures += 1
    else:
        # Already logged above, no need to log again.
        pass

    print("\n------------------------------------------------")
    if failures == 0:
        print("READY TO SUBMIT")
        print("🚀 All checks passed. You are ready to submit to OpenEnv Hackathon.")
    else:
        print(f"NOT READY ({failures} failures)")

if __name__ == "__main__":
    main()

