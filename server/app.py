import uvicorn
import os
import sys

# Ensure the root directory is accessible so env.py and others resolve normally.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import app

def start():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    start()
