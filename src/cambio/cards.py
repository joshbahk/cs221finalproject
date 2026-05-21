from dataclasses import dataclass

@dataclass(frozen=True)
class Card: 
    rank: str
    suit: str

    def short_name(self) -> str: 
        if self.rank == "JOKER": 
            return "JOKER"
        suit_symbol = {"hearts": "H", "diamonds": "D", "clubs": "C", "spades":"S"}[self.suit]
        return f"{self.rank}{suit_symbol}"



def make_deck(include_jokers: bool = True) -> list[Card]:
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["hearts", "diamonds", "clubs", "spades"]

    deck = [Card(rank, suit) for rank in ranks for suit in suits]

    if include_jokers:
        deck.append(Card("JOKER", "joker"))
        deck.append(Card("JOKER", "joker"))

    return deck


def card_value(card: Card) -> int:
    if card.rank == "JOKER":
        return 0

    if card.rank == "A":
        return 1

    if card.rank in {"J", "Q"}:
        return 10

    if card.rank == "K":
        if card.suit in {"hearts", "diamonds"}:
            return -1
        return 10

    return int(card.rank)


def card_power(card: Card) -> str | None:
    if card.rank in {"7", "8"}:
        return "peek_self"

    if card.rank in {"9", "10"}:
        return "peek_opponent"

    if card.rank in {"J", "Q"}:
        return "blind_swap"

    if card.rank == "K" and card.suit in {"clubs", "spades"}:
        return "king_swap"

    return None