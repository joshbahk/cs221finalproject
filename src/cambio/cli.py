from cambio.agents import Agent, RandomAgent
from cambio.env import CambioEnv


def _format_card(card) -> str:
    return "?" if card is None else card.short_name()


def _format_action(action) -> str:
    params = dict(action.params)
    if not params:
        return action.kind
    ordered = ", ".join(f"{key}={value}" for key, value in params.items())
    return f"{action.kind}({ordered})"


class HumanAgent(Agent):
    name = "human"

    def choose_action(self, observation, legal_actions):
        print("\n=== Your Turn ===")
        print(f"phase: {observation.phase}")
        print(f"your cards: {[ _format_card(card) for card in observation.my_cards ]}")
        print(f"opponent cards: {[ _format_card(card) for card in observation.opponent_cards ]}")
        print(f"discard top: {_format_card(observation.discard_top)}")
        print(f"deck size: {observation.deck_size}")
        if observation.drawn_card is not None:
            print(f"drawn card: {_format_card(observation.drawn_card)}")

        print("\nlegal actions:")
        for idx, action in enumerate(legal_actions):
            print(f"  [{idx}] {_format_action(action)}")

        while True:
            raw = input("Choose action index: ").strip()
            if not raw.isdigit():
                print("Please enter a valid numeric index.")
                continue
            choice = int(raw)
            if 0 <= choice < len(legal_actions):
                return legal_actions[choice]
            print("Index out of range. Try again.")


def run_cli(seed: int | None = None) -> None:
    env = CambioEnv(seed=seed)
    env.reset()

    players: dict[int, Agent] = {
        0: HumanAgent(),
        1: RandomAgent(seed=seed),
    }

    while not env.is_terminal():
        player_id = env.state.current_player
        legal = env.legal_actions(player_id)
        observation = env.get_observation(player_id)
        action = players[player_id].choose_action(observation, legal)

        if player_id == 1:
            print(f"\nBot chose: {_format_action(action)}")

        env.step(action)

    print("\n=== Game Over ===")
    for pid, player in enumerate(env.state.players):
        print(f"player {pid} hand: {[card.short_name() for card in player.hand]}")
    scores = env.final_scores()
    print(f"scores: {scores}")
    if scores[0] < scores[1]:
        print("You win.")
    elif scores[1] < scores[0]:
        print("Bot wins.")
    else:
        print("Tie.")


if __name__ == "__main__":
    run_cli()
