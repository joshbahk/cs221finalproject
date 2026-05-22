from cambio.agents import RandomAgent
from cambio.env import CambioEnv
from cambio.simulate import play_game


def test_random_game_produces_result():
    env = CambioEnv(seed=0)
    agents = [RandomAgent(seed=1), RandomAgent(seed=2)]

    trajectory, result = play_game(env, agents, game_id=0, max_steps=200)

    assert isinstance(trajectory, list)
    assert result["type"] == "game_result"
    assert len(result["final_scores"]) == 2
    assert len(result["utilities"]) == 2
    assert result["winner"] in {0, 1}
    assert result["num_turns"] <= 200