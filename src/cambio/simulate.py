from __future__ import annotations

from typing import Any

from cambio.env import CambioEnv


def play_game(
    env: CambioEnv,
    agents,
    game_id: int = 0,
    max_steps: int = 200,
    log: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Play one complete two-player Cambio game.

    Args:
        env: The Cambio environment.
        agents: A list of agents, one per player.
        game_id: ID used for logging.
        max_steps: Failsafe to stop games that do not naturally terminate.
        log: Whether to record transition rows.

    Returns:
        trajectory: A list of transition dictionaries.
        result: A dictionary with final scores, utilities, winner, etc.
    """
    env.reset()
    trajectory: list[dict[str, Any]] = []

    steps = 0

    while not env.is_terminal() and steps < max_steps:
        player_id = env.state.current_player
        observation = env.get_observation(player_id)
        legal_actions = env.legal_actions(player_id)

        if not legal_actions:
            raise RuntimeError(
                f"No legal actions for player={player_id}, "
                f"phase={env.state.phase}, done={env.state.done}"
            )

        action = agents[player_id].choose_action(observation, legal_actions)

        if log:
            trajectory.append(
                {
                    "type": "transition",
                    "game_id": game_id,
                    "turn": steps,
                    "player": player_id,
                    "observation": observation.to_json(),
                    "legal_actions": [a.to_json() for a in legal_actions],
                    "action": action.to_json(),
                    "phase": observation.phase,
                }
            )

        env.step(action)
        steps += 1

    if not env.is_terminal():
        env.state.done = True

    scores = env.final_scores()
    utilities = env.utilities()
    winner = min(range(env.num_players), key=lambda p: scores[p])

    result = {
        "type": "game_result",
        "game_id": game_id,
        "final_scores": scores,
        "utilities": utilities,
        "winner": winner,
        "num_turns": steps,
        "agents": [agent.name for agent in agents],
        "cambio_called_by": env.state.cambio_called_by,
        "ended_by_max_steps": steps >= max_steps,
    }

    return trajectory, result