import pytest

from cambio.actions import Action
from cambio.cards import Card
from cambio.env import CambioEnv


def test_step_rejects_illegal_action():
    env = CambioEnv(seed=1)
    env.reset()

    with pytest.raises(ValueError):
        env.step(Action.make("replace_self", slot=0))


def test_draw_then_replace_advances_turn_when_no_power():
    env = CambioEnv(seed=1)
    env.reset()

    env.state.phase = "after_draw_deck"
    env.state.drawn_card = Card("5", "hearts")
    current = env.state.current_player

    env.step(Action.make("replace_self", slot=0))

    assert env.state.phase == "start_turn"
    assert env.state.current_player == 1 - current
    assert env.state.drawn_card is None


def test_power_resolution_peek_opponent_updates_knowledge():
    env = CambioEnv(seed=1)
    env.reset()
    actor = env.state.current_player
    opponent = 1 - actor

    env.state.phase = "after_draw_deck"
    env.state.drawn_card = Card("9", "clubs")

    env.step(Action.make("replace_self", slot=0))
    assert env.state.phase == "power_resolution"

    env.step(Action.make("peek_opponent", opponent=opponent, slot=0))

    assert 0 in env.state.players[actor].known_opp_cards
    assert env.state.phase == "start_turn"
    assert env.state.current_player == opponent


def test_call_cambio_then_opponent_turn_ends_game():
    env = CambioEnv(seed=1)
    env.reset()

    env.state.deck = [Card("5", "hearts")]
    env.step(Action.make("call_cambio"))
    assert env.state.cambio_called_by == 0
    assert env.state.final_turns_remaining == 1

    env.step(Action.make("draw_deck"))
    env.step(Action.make("discard_drawn"))

    assert env.is_terminal()
    scores = env.final_scores()
    utils = env.utilities()
    assert len(scores) == 2
    assert len(utils) == 2
