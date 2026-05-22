from __future__ import annotations

from statistics import mean
from time import perf_counter

from cambio.env import CambioEnv
from cambio.registry import make_agent
from cambio.simulate import play_game


def evaluate_matchup(
    agent_a: str,
    agent_b: str,
    games: int = 100,
    seed: int = 0,
    max_steps: int = 200,
) -> dict:
    a_wins = 0
    a_utilities = []
    b_utilities = []
    a_scores = []
    b_scores = []
    turns = []
    max_step_games = 0

    start = perf_counter()

    for game_id in range(games):
        env = CambioEnv(seed=seed + game_id)

        agents = [
            make_agent(agent_a, seed=seed + 10_000 + game_id),
            make_agent(agent_b, seed=seed + 20_000 + game_id),
        ]

        _, result = play_game(
            env=env,
            agents=agents,
            game_id=game_id,
            max_steps=max_steps,
            log=False,
        )

        if result["winner"] == 0:
            a_wins += 1

        a_utilities.append(result["utilities"][0])
        b_utilities.append(result["utilities"][1])
        a_scores.append(result["final_scores"][0])
        b_scores.append(result["final_scores"][1])
        turns.append(result["num_turns"])

        if result["ended_by_max_steps"]:
            max_step_games += 1

    elapsed_s = perf_counter() - start

    return {
        "agent_a": agent_a,
        "agent_b": agent_b,
        "games": games,
        "a_win_rate": a_wins / games,
        "a_avg_utility": mean(a_utilities),
        "b_avg_utility": mean(b_utilities),
        "a_avg_score": mean(a_scores),
        "b_avg_score": mean(b_scores),
        "avg_turns": mean(turns),
        "max_step_games": max_step_games,
        "elapsed_s": elapsed_s,
        "games_per_second": games / elapsed_s if elapsed_s > 0 else 0,
    }