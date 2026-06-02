import sys
from pathlib import Path

# file path putting root node 
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cambio.env import CambioEnv
from cambio.actions import Action

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = CambioEnv(seed=42)
env.reset()

#pulls state from observation
@app.get("/state")
def get_state():
    obs = env.get_observation(0)

    return {
        "observation": obs.to_json(),
        "legal_actions": [
            action.to_json()
            for action in env.legal_actions(0)
        ],
    }

#resetting the game
@app.post("/reset")
def reset():
    env.reset()

    return {"success": True}

#taking an action
@app.post("/action")
def perform_action(action_data: dict):

    action = Action.make(
        action_data["kind"],
        **action_data.get("params", {})
    )
    env.step(action)
    return {"success": True}