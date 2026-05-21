from dataclasses import dataclass, field
from cambio.cards import Card


@dataclass
class PlayerState:
    hand: list[Card]
    known_self_slots: set[int] = field(default_factory=set)
    known_opp_cards: dict[int, Card] = field(default_factory=dict)


@dataclass
class GameState:
    players: list[PlayerState]
    deck: list[Card]
    discard_pile: list[Card]
    current_player: int
    phase: str
    drawn_card: Card | None
    cambio_called_by: int | None
    final_turns_remaining: int | None
    turn_count: int
    done: bool


@dataclass
class Observation:
    player_id: int
    my_cards: list[Card | None]
    opponent_cards: list[Card | None]
    discard_top: Card | None
    deck_size: int
    phase: str
    drawn_card: Card | None
    cambio_called_by: int | None
    final_turns_remaining: int | None
    turn_count: int

    def to_json(self) -> dict:
        def card_to_json(card):
            return None if card is None else card.short_name()

        return {
            "player_id": self.player_id,
            "my_cards": [card_to_json(card) for card in self.my_cards],
            "opponent_cards": [card_to_json(card) for card in self.opponent_cards],
            "discard_top": card_to_json(self.discard_top),
            "deck_size": self.deck_size,
            "phase": self.phase,
            "drawn_card": card_to_json(self.drawn_card),
            "cambio_called_by": self.cambio_called_by,
            "final_turns_remaining": self.final_turns_remaining,
            "turn_count": self.turn_count,
        }