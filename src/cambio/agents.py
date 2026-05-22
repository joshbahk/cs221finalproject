import copy
import random

from cambio.cards import card_value, make_deck
from cambio.env import CambioEnv
from cambio.state import GameState, PlayerState


class Agent:
    name = "base"

    def choose_action(self, observation, legal_actions):
        raise NotImplementedError


class RandomAgent(Agent):
    name = "random"

    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def choose_action(self, observation, legal_actions):
        return self.rng.choice(legal_actions)
def remove_one_card(deck, target):
    for i, card in enumerate(deck):
        if card == target:
            deck.pop(i)
            return

    raise ValueError(f"Could not remove card {target}")


def sample_env_from_observation(observation, seed=None) -> CambioEnv:
    """
    Sample on e ull Cambio environment consistent with the player's observation

    The agent only receives an Observation -- creates one plausible hidden world that agrees with all known cards
    """
    rng = random.Random(seed)
    deck = make_deck(include_jokers=True)

    known_cards = []

    for card in observation.my_cards:
        if card is not None:
            known_cards.append(card)

    for card in observation.opponent_cards:
        if card is not None:
            known_cards.append(card)

    if observation.discard_top is not None:
        known_cards.append(observation.discard_top)

    if observation.drawn_card is not None:
        known_cards.append(observation.drawn_card)

    for card in known_cards:
        remove_one_card(deck, card)

    rng.shuffle(deck)

    my_hand = []
    my_known_self_slots = set()

    for slot, card in enumerate(observation.my_cards):
        if card is None:
            my_hand.append(deck.pop())
        else:
            my_hand.append(card)
            my_known_self_slots.add(slot)

    opponent_hand = []
    my_known_opp_cards = {}

    for slot, card in enumerate(observation.opponent_cards):
        if card is None:
            opponent_hand.append(deck.pop())
        else:
            opponent_hand.append(card)
            my_known_opp_cards[slot] = card

    root_player = observation.player_id

    if root_player == 0:
        players = [
            PlayerState(
                hand=my_hand,
                known_self_slots=my_known_self_slots,
                known_opp_cards=my_known_opp_cards,
            ),
            PlayerState(
                hand=opponent_hand,
                known_self_slots=set(),
                known_opp_cards={},
            ),
        ]
    else:
        players = [
            PlayerState(
                hand=opponent_hand,
                known_self_slots=set(),
                known_opp_cards={},
            ),
            PlayerState(
                hand=my_hand,
                known_self_slots=my_known_self_slots,
                known_opp_cards=my_known_opp_cards,
            ),
        ]

    env = CambioEnv(seed=seed)

    env.state = GameState(
        players=players,
        deck=deck[: observation.deck_size],
        discard_pile=[observation.discard_top] if observation.discard_top else [],
        current_player=observation.player_id,
        phase=observation.phase,
        drawn_card=observation.drawn_card,
        cambio_called_by=observation.cambio_called_by,
        final_turns_remaining=observation.final_turns_remaining,
        turn_count=observation.turn_count,
        done=False,
    )

    return env


def evaluate_env(env: CambioEnv, root_player: int) -> float:
    """
    Depth-limited evaluation function

    utility = opponent_score - my_score

    Positive is good for root_player.
    """
    scores = env.final_scores()

    if root_player == 0:
        return scores[1] - scores[0]

    return scores[0] - scores[1]


def random_opponent_distribution(env: CambioEnv):
    """
    model the opponent as uniformly random over legal actions.
    """
    player_id = env.state.current_player
    legal_actions = env.legal_actions(player_id)

    if not legal_actions:
        return []

    probability = 1.0 / len(legal_actions)
    return [(action, probability) for action in legal_actions]


def expectimax_value(
    env: CambioEnv,
    root_player: int,
    depth: int,
) -> float:
    """
    Depth-limited expectimax.

    Cases:
        terminal state:
            return utility

        depth == 0:
            return evaluation function

        root player's turn:
            max over actions

        opponent's turn:
            expectation over fixed random opponent policy
    """
    if env.is_terminal():
        return env.utilities()[root_player]

    if depth == 0:
        return evaluate_env(env, root_player)

    current_player = env.state.current_player
    legal_actions = env.legal_actions(current_player)

    if not legal_actions:
        return evaluate_env(env, root_player)

    if current_player == root_player:
        best_value = float("-inf")

        for action in legal_actions:
            next_env = copy.deepcopy(env)
            next_env.step(action)

            value = expectimax_value(
                env=next_env,
                root_player=root_player,
                depth=depth - 1,
            )

            best_value = max(best_value, value)

        return best_value

    expected_value = 0.0

    for action, probability in random_opponent_distribution(env):
        next_env = copy.deepcopy(env)
        next_env.step(action)

        value = expectimax_value(
            env=next_env,
            root_player=root_player,
            depth=depth - 1,
        )

        expected_value += probability * value

    return expected_value


class ExpectimaxAgent(Agent):
    name = "expectimax"

    def __init__(
        self,
        depth: int = 2,
        num_world_samples: int = 5,
        seed=None,
    ):
        self.depth = depth
        self.num_world_samples = num_world_samples
        self.rng = random.Random(seed)

    def choose_action(self, observation, legal_actions):
        """
        Choose action with the highest average expectimax value

        we sample several possible hidden worlds
        consistent with the observation, run expectimax in each world, and average
        """
        action_values = {}

        for action in legal_actions:
            total_value = 0.0

            for _ in range(self.num_world_samples):
                sampled_env = sample_env_from_observation(
                    observation=observation,
                    seed=self.rng.randint(0, 10**9),
                )

                try:
                    sampled_env.step(action)
                except Exception:
                    total_value += float("-inf")
                    continue

                value = expectimax_value(
                    env=sampled_env,
                    root_player=observation.player_id,
                    depth=self.depth,
                )

                total_value += value

            action_values[action] = total_value / self.num_world_samples

        return max(action_values, key=action_values.get)