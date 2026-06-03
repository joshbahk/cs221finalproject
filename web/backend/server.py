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
from cambio.agents import RandomAgent, ExpectimaxAgent, MonteCarloAgent
from cambio.cards import card_value

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
    "expectimax": lambda: ExpectimaxAgent(seed=42),
    "montecarlo": lambda: MonteCarloAgent(seed=42),
}

bot = AGENTS["random"]()

env = CambioEnv(seed=42)
env.reset()


@app.get("/agents")
def list_agents():
    return {"agents": list(AGENTS.keys())}

def hand_score(player):
    return sum(card_value(c) for c in player.hand if c is not None)

@app.get("/state")
def get_state():
    obs = env.get_observation(0)
    result = {
        "observation": obs.to_json(),
        "legal_actions": [action.to_json() for action in env.legal_actions(0)],
        "done": env.is_terminal(),
    }
    if env.is_terminal():
        from cambio.cards import card_value
        result["scores"] = {
        "you": hand_score(env.state.players[0]),
        "opponent": hand_score(env.state.players[1]),
        }
    return result

@app.post("/reset")
def reset(agent: str = "random"):
    global bot
    if agent not in AGENTS:
        return {"success": False, "error": f"Unknown agent: {agent}"}
    bot = AGENTS[agent]()
    env.reset()
    return {"success": True}


@app.post("/action")
def perform_action(action_data: dict):
    action = Action.make(action_data["kind"], **action_data.get("params", {}))
    env.step(action)

    while not env.is_terminal() and env.state.current_player == 1:
        obs = env.get_observation(1)
        legal = env.legal_actions(1)
        bot_action = bot.choose_action(obs, legal)
        env.step(bot_action)

    return {"success": True}