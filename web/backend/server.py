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


@app.post("/reset")
def reset():
    env.reset()

    return {"success": True}


@app.post("/action")
def perform_action(action_data: dict):

    action = Action.make(
        action_data["kind"],
        **action_data.get("params", {})
    )

    env.step(action)

    return {"success": True}