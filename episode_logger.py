import threading
from typing import Dict, List, Any
from copy import deepcopy

class EpisodeLogger:
    """Thread-safe episode logger buffering actions, rewards, and constraints linearly."""
    def __init__(self):
        self.lock = threading.Lock()
        self.episodes: List[Dict[str, Any]] = []
        self.current_episode: Dict[str, Any] = None
        
    def start_episode(self, task_config: Dict[str, Any], initial_portfolio_value: float):
        with self.lock:
            self.current_episode = {
                "actions": [],
                "rewards": [],
                "portfolio_values": [initial_portfolio_value],
                "initial_portfolio_value": initial_portfolio_value,
                "task_config": deepcopy(task_config),
                "steps_taken": 0,
                "final_portfolio_value": initial_portfolio_value
            }

    def log_step(self, action: Dict[str, Any], reward: float, portfolio_value: float):
        with self.lock:
            if self.current_episode is not None:
                self.current_episode["actions"].append(deepcopy(action))
                self.current_episode["rewards"].append(reward)
                self.current_episode["portfolio_values"].append(portfolio_value)
                self.current_episode["steps_taken"] += 1
                self.current_episode["final_portfolio_value"] = portfolio_value

    def end_episode(self) -> Dict[str, Any]:
        with self.lock:
            if self.current_episode is not None:
                ep_log = deepcopy(self.current_episode)
                self.episodes.append(ep_log)
                if len(self.episodes) > 10:
                    self.episodes.pop(0)
                self.current_episode = None
                return ep_log
            return {}

    def get_last_episodes(self) -> List[Dict[str, Any]]:
        with self.lock:
            return deepcopy(self.episodes)

