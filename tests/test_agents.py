from cambio.agents import ExpectimaxAgent, RandomAgent
from cambio.env import CambioEnv


def test_random_agent_returns_legal_action():
    env = CambioEnv(seed=0)
    env.reset()

    obs = env.get_observation(0)
    legal_actions = env.legal_actions(0)

    action = RandomAgent(seed=0).choose_action(obs, legal_actions)

    assert action in legal_actions


def test_expectimax_agent_returns_legal_action():
    env = CambioEnv(seed=0)
    env.reset()

    obs = env.get_observation(0)
    legal_actions = env.legal_actions(0)

    agent = ExpectimaxAgent(
        depth=1,
        num_world_samples=1,
        seed=0,
    )

    action = agent.choose_action(obs, legal_actions)

    assert action in legal_actions