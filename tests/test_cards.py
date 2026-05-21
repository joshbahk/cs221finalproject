from cambio.cards import Card, make_deck, card_value, card_power


def test_deck_size_with_jokers():
    deck = make_deck(include_jokers=True)
    assert len(deck) == 54


def test_deck_size_without_jokers():
    deck = make_deck(include_jokers=False)
    assert len(deck) == 52


def test_card_values():
    assert card_value(Card("A", "hearts")) == 1
    assert card_value(Card("2", "clubs")) == 2
    assert card_value(Card("Q", "spades")) == 10
    assert card_value(Card("K", "hearts")) == -1
    assert card_value(Card("K", "diamonds")) == -1
    assert card_value(Card("K", "clubs")) == 10
    assert card_value(Card("JOKER", "joker")) == 0


def test_card_powers():
    assert card_power(Card("7", "hearts")) == "peek_self"
    assert card_power(Card("9", "clubs")) == "peek_opponent"
    assert card_power(Card("J", "spades")) == "blind_swap"
    assert card_power(Card("K", "spades")) == "king_swap"
    assert card_power(Card("K", "hearts")) is None
    assert card_power(Card("5", "diamonds")) is None