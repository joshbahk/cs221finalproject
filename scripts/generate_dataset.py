import argparse
import json
from pathlib import Path

from tqdm import tqdm

from cambio.env import CambioEnv
from cambio.registry import make_agent
from cambio.simulate import play_game


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-a", default="expectimax")
    parser.add_argument("--agent-b", default="random")
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", default="data/self_play.jsonl")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_transitions = 0
    total_max_step_games = 0

    with out_path.open("w", encoding="utf-8") as f:
        for game_id in tqdm(range(args.games)):
            env = CambioEnv(seed=args.seed + game_id)

            agents = [
                make_agent(args.agent_a, seed=args.seed + 10_000 + game_id),
                make_agent(args.agent_b, seed=args.seed + 20_000 + game_id),
            ]

            trajectory, result = play_game(
                env=env,
                agents=agents,
                game_id=game_id,
                log=True,
            )

            total_transitions += len(trajectory)

            if result["ended_by_max_steps"]:
                total_max_step_games += 1

            for row in trajectory:
                f.write(json.dumps(row) + "\n")

            f.write(json.dumps(result) + "\n")

    print("Wrote:", out_path)
    print("Games:", args.games)
    print("Transitions:", total_transitions)
    print("Average turns:", total_transitions / args.games)
    print("Max-step games:", total_max_step_games)


if __name__ == "__main__":
    main()