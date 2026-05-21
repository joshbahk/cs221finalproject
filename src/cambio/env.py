import random
from cambio.actions import Action
from cambio.cards import make_deck, card_value, card_power
from cambio.state import GameState, PlayerState, Observation


class CambioEnv:
    def __init__(self, num_players: int = 2, seed: int | None = None):
        if num_players != 2:
            raise NotImplementedError("MVP only supports two players.")

        self.num_players = num_players
        self.rng = random.Random(seed)
        self.state: GameState | None = None

    def reset(self) -> GameState:
        deck = make_deck(include_jokers=True)
        self.rng.shuffle(deck)

        players = []
        for _ in range(self.num_players):
            hand = [deck.pop() for _ in range(4)]
            players.append(PlayerState(
                hand=hand,
                known_self_slots={0, 1},
                known_opp_cards={},
            ))

        discard_pile = [deck.pop()]

        self.state = GameState(
            players=players,
            deck=deck,
            discard_pile=discard_pile,
            current_player=0,
            phase="start_turn",
            drawn_card=None,
            cambio_called_by=None,
            final_turns_remaining=None,
            turn_count=0,
            done=False,
        )

        return self.state

    def get_observation(self, player_id: int) -> Observation:
        assert self.state is not None

        player = self.state.players[player_id]
        opponent_id = 1 - player_id
        opponent = self.state.players[opponent_id]

        my_cards = []
        for slot, card in enumerate(player.hand):
            if slot in player.known_self_slots:
                my_cards.append(card)
            else:
                my_cards.append(None)

        opponent_cards = []
        for slot, card in enumerate(opponent.hand):
            if slot in player.known_opp_cards:
                opponent_cards.append(player.known_opp_cards[slot])
            else:
                opponent_cards.append(None)

        discard_top = self.state.discard_pile[-1] if self.state.discard_pile else None

        return Observation(
            player_id=player_id,
            my_cards=my_cards,
            opponent_cards=opponent_cards,
            discard_top=discard_top,
            deck_size=len(self.state.deck),
            phase=self.state.phase,
            drawn_card=self.state.drawn_card,
            cambio_called_by=self.state.cambio_called_by,
            final_turns_remaining=self.state.final_turns_remaining,
            turn_count=self.state.turn_count,
        )

    def is_terminal(self) -> bool:
        assert self.state is not None
        return self.state.done

    def final_scores(self) -> list[int]:
        assert self.state is not None
        return [
            sum(card_value(card) for card in player.hand)
            for player in self.state.players
        ]

    def utilities(self) -> list[int]:
        scores = self.final_scores()
        return [
            scores[1] - scores[0],
            scores[0] - scores[1],
        ]
    

    def legal_actions(self, player_id: int) -> list[Action]:
        assert self.state is not None

        if self.state.done:
            return []

        if player_id != self.state.current_player:
            return []

        if self.state.phase == "start_turn":
            actions = [Action.make("draw_deck")]

            if self.state.discard_pile:
                actions.append(Action.make("draw_discard"))

            if self.state.cambio_called_by is None:
                actions.append(Action.make("call_cambio"))

            return actions

        if self.state.phase == "after_draw_deck":
            actions = [
                Action.make("replace_self", slot=slot)
                for slot in range(4)
            ]
            actions.append(Action.make("discard_drawn"))
            return actions

        if self.state.phase == "after_draw_discard":
            return [
                Action.make("replace_self", slot=slot)
                for slot in range(4)
            ]

        if self.state.phase == "power_resolution":
            power = card_power(self.state.drawn_card)
            opponent_id = 1 - player_id

            if power == "peek_self":
                return [
                    Action.make("peek_self", slot=slot)
                    for slot in range(4)
                ]

            if power == "peek_opponent":
                return [
                    Action.make("peek_opponent", opponent=opponent_id, slot=slot)
                    for slot in range(4)
                ]

            if power == "blind_swap":
                return [
                    Action.make("blind_swap", my_slot=my_slot, opponent=opponent_id, opp_slot=opp_slot)
                    for my_slot in range(4)
                    for opp_slot in range(4)
                ]

            if power == "king_swap":
                return [
                    Action.make("king_swap", my_slot=my_slot, opponent=opponent_id, opp_slot=opp_slot)
                    for my_slot in range(4)
                    for opp_slot in range(4)
                ]

        return []