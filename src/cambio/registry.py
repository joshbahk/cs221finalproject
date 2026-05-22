from cambio.agents import ExpectimaxAgent, RandomAgent


AGENT_REGISTRY = {
    "random": {
        "class": RandomAgent,
        "description": "Uniform random legal-action baseline.",
    },
    "expectimax": {
        "class": ExpectimaxAgent,
        "description": "Depth-limited expectimax agent with sampled hidden worlds.",
    },
}


def make_agent(name: str, seed: int | None = None):
    if name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent={name}. Options: {list(AGENT_REGISTRY)}")

    cls = AGENT_REGISTRY[name]["class"]

    try:
        return cls(seed=seed)
    except TypeError:
        return cls()