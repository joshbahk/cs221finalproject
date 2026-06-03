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
    Sample one possible full Cambio environment consistent with the player's observation.

    The real game has hidden cards. The agent only receives an Observation.
    This function creates one plausible hidden world that agrees with all known cards.

    Important detail:
    Sometimes the same physical card can appear both as drawn_card and inside
    my_cards during power resolution. We should only remove each known physical
    card once from the sampled deck.
    """
    rng = random.Random(seed)
    deck = make_deck(include_jokers=True)

    known_cards = []

    def add_known_card(card):
        if card is None:
            return

        # Non-joker cards are unique in the deck, so do not add duplicates.
        # Jokers are not unique, so if both jokers are truly visible, allowing
        # duplicates is okay.
        if card.rank != "JOKER" and card in known_cards:
            return

        known_cards.append(card)

    for card in observation.my_cards:
        add_known_card(card)

    for card in observation.opponent_cards:
        add_known_card(card)

    add_known_card(observation.discard_top)
    add_known_card(observation.drawn_card)

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


def _greedy_rollout_action(env: CambioEnv, legal_actions, rng: random.Random):
    """
    Small heuristic for the search player's own moves inside a rollout. After drawing,
    replace worst card if the drawn card beats it, otherwise discard.
    Everything else stays random.
    """
    state = env.state
    player_id = state.current_player

    if state.phase in ("after_draw_deck", "after_draw_discard") and state.drawn_card is not None:
        values = [card_value(card) for card in state.players[player_id].hand]
        worst_slot = max(range(len(values)), key=lambda s: values[s])

        if card_value(state.drawn_card) < values[worst_slot]:
            for action in legal_actions:
                if action.kind == "replace_self" and action.get("slot") == worst_slot:
                    return action

        for action in legal_actions:
            if action.kind == "discard_drawn":
                return action

    return rng.choice(legal_actions)


def rollout_value(
    env: CambioEnv,
    root_player: int,
    rng: random.Random,
    max_plies: int = 200,
) -> float:
    """
    Monte Carlo rollout.

    Instead of expansively exploring the tree, play one playout to the end and
    return the result. The opponent plays randomly for our model and includes
    greedy heuristic for better win rate.
    """
    plies = 0

    while not env.is_terminal() and plies < max_plies:
        current_player = env.state.current_player
        legal_actions = env.legal_actions(current_player)

        if not legal_actions:
            break

        if current_player == root_player:
            action = _greedy_rollout_action(env, legal_actions, rng)
        else:
            action = rng.choice(legal_actions)

        env.step(action)
        plies += 1

    if env.is_terminal():
        return env.utilities()[root_player]

    return evaluate_env(env, root_player)


class MonteCarloAgent(Agent):
    name = "montecarlo"

    def __init__(
        self,
        num_world_samples: int = 30,
        seed=None,
    ):
        self.num_world_samples = num_world_samples
        self.rng = random.Random(seed)

    def choose_action(self, observation, legal_actions):
        """
        Choose action with the highest average rollout value.

        Similar to Expectimax, but uses Monte Carlo rollouts.
        """
        action_values = {}

        for action in legal_actions:
            total_value = 0.0
            num_evaluated = 0

            for _ in range(self.num_world_samples):
                try:
                    sampled_env = sample_env_from_observation(
                        observation=observation,
                        seed=self.rng.randint(0, 10**9),
                    )
                    sampled_env.step(action)
                except Exception:
                    continue

                total_value += rollout_value(
                    env=sampled_env,
                    root_player=observation.player_id,
                    rng=self.rng,
                )
                num_evaluated += 1

            action_values[action] = (
                total_value / num_evaluated if num_evaluated else float("-inf")
            )

        return max(action_values, key=action_values.get)