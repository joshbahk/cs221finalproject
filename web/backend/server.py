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
from cambio.agents import RandomAgent, ExpectimaxAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AGENTS = {
    "random": lambda: RandomAgent(seed=42),
    "expectimax": lambda: ExpectimaxAgent(depth=2, num_world_samples=5, seed=42),
}

env = CambioEnv(seed=42)
bot = AGENTS["random"]()
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
        "done": env.is_terminal(),
    }

#resetting the game
@app.post("/reset")
def reset(agent: str = "random"):
    global bot
    if agent not in AGENTS:
        return {"success": False, "error": f"Unknown agent: {agent}"}
    bot = AGENTS[agent]()
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
    

    while not env.is_terminal() and env.state.current_player == 1:
        obs = env.get_observation(1)
        legal = env.legal_actions(1)
        bot_action = bot.choose_action(obs, legal)
        env.step(bot_action)
    return {"success": True}
 