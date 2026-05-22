import argparse
import csv
from pathlib import Path

from cambio.evaluation import evaluate_matchup


def parse_matchups(text: str) -> list[tuple[str, str]]:
    pairs = []

    for item in text.split(","):
        item = item.strip()
        if not item:
            continue

        agent_a, agent_b = item.split(":")
        pairs.append((agent_a.strip(), agent_b.strip()))

    return pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matchups",
        default="random:random,expectimax:random",
        help="Comma-separated matchups, e.g. random:random,expectimax:random",
    )
    parser.add_argument("--games", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", default="results/matchup_results.csv")
    args = parser.parse_args()

    results = []

    for agent_a, agent_b in parse_matchups(args.matchups):
        print(f"Running {agent_a} vs {agent_b} for {args.games} games...")

        result = evaluate_matchup(
            agent_a=agent_a,
            agent_b=agent_b,
            games=args.games,
            seed=args.seed,
        )

        print(result)
        results.append(result)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    print("Wrote:", out_path)


if __name__ == "__main__":
    main()