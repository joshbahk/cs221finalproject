from cambio.agents import RandomAgent
from cambio.env import CambioEnv
from cambio.simulate import play_game


def main():
    env = CambioEnv(seed=0)
    agents = [
        RandomAgent(seed=1),
        RandomAgent(seed=2),
    ]

    trajectory, result = play_game(env, agents, game_id=0)

    print("Game finished.")
    print("Transitions:", len(trajectory))
    print("Result:")
    print(result)


if __name__ == "__main__":
    main()