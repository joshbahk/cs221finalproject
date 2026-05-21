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

    def step(self, action: Action) -> GameState:
        assert self.state is not None
        if self.state.done:
            raise ValueError("Cannot step when game is terminal.")

        self._require_legal_action(action)

        if self.state.phase == "start_turn":
            self._handle_start_turn_action(action)
            return self.state

        if self.state.phase in {"after_draw_deck", "after_draw_discard"}:
            self._handle_after_draw_action(action)
            return self.state

        if self.state.phase == "power_resolution":
            self._handle_power_resolution_action(action)
            return self.state

        raise ValueError(f"Unknown phase: {self.state.phase}")

    def legal_actions(self, player_id: int) -> list[Action]:
        assert self.state is not None

        if self.state.done:
            return []

        if player_id != self.state.current_player:
            return []

        if self.state.phase == "start_turn":
            actions = []
            if self.state.deck:
                actions.append(Action.make("draw_deck"))

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
            if self.state.drawn_card is None:
                return []

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

    def _require_legal_action(self, action: Action) -> None:
        assert self.state is not None
        legal = set(self.legal_actions(self.state.current_player))
        if action not in legal:
            raise ValueError(f"Illegal action for current phase: {action.to_json()}")

    def _handle_start_turn_action(self, action: Action) -> None:
        assert self.state is not None
        if action.kind == "draw_deck":
            self.state.drawn_card = self.state.deck.pop()
            self.state.phase = "after_draw_deck"
            return

        if action.kind == "draw_discard":
            self.state.drawn_card = self.state.discard_pile.pop()
            self.state.phase = "after_draw_discard"
            return

        if action.kind == "call_cambio":
            self.state.cambio_called_by = self.state.current_player
            self.state.final_turns_remaining = self.num_players - 1
            self._advance_turn()
            return

        raise ValueError(f"Unhandled start_turn action kind: {action.kind}")

    def _handle_after_draw_action(self, action: Action) -> None:
        assert self.state is not None
        if self.state.drawn_card is None:
            raise ValueError("drawn_card must be set in draw resolution phases.")

        if action.kind == "replace_self":
            slot = action.get("slot")
            if not isinstance(slot, int) or not (0 <= slot < 4):
                raise ValueError("replace_self requires slot in [0, 3].")

            player = self.state.players[self.state.current_player]
            replaced = player.hand[slot]
            player.hand[slot] = self.state.drawn_card
            player.known_self_slots.add(slot)
            self.state.discard_pile.append(replaced)
            self._post_draw_resolution()
            return

        if action.kind == "discard_drawn":
            self.state.discard_pile.append(self.state.drawn_card)
            self._post_draw_resolution()
            return

        raise ValueError(f"Unhandled post-draw action kind: {action.kind}")

    def _post_draw_resolution(self) -> None:
        assert self.state is not None
        assert self.state.drawn_card is not None
        power = card_power(self.state.drawn_card)
        if power is None:
            self.state.drawn_card = None
            self._advance_turn()
            return

        self.state.phase = "power_resolution"

    def _handle_power_resolution_action(self, action: Action) -> None:
        assert self.state is not None
        if self.state.drawn_card is None:
            raise ValueError("No drawn card available for power resolution.")

        actor_id = self.state.current_player
        opponent_id = 1 - actor_id
        actor = self.state.players[actor_id]
        opponent = self.state.players[opponent_id]
        kind = action.kind

        if kind == "peek_self":
            slot = action.get("slot")
            if not isinstance(slot, int) or not (0 <= slot < 4):
                raise ValueError("peek_self requires slot in [0, 3].")
            actor.known_self_slots.add(slot)

        elif kind == "peek_opponent":
            slot = action.get("slot")
            if not isinstance(slot, int) or not (0 <= slot < 4):
                raise ValueError("peek_opponent requires slot in [0, 3].")
            actor.known_opp_cards[slot] = opponent.hand[slot]

        elif kind in {"blind_swap", "king_swap"}:
            my_slot = action.get("my_slot")
            opp_slot = action.get("opp_slot")
            if (
                not isinstance(my_slot, int)
                or not isinstance(opp_slot, int)
                or not (0 <= my_slot < 4)
                or not (0 <= opp_slot < 4)
            ):
                raise ValueError(f"{kind} requires my_slot/opp_slot in [0, 3].")

            actor.hand[my_slot], opponent.hand[opp_slot] = opponent.hand[opp_slot], actor.hand[my_slot]

            actor.known_opp_cards.pop(opp_slot, None)
            opponent.known_opp_cards.pop(my_slot, None)

            if kind == "blind_swap":
                actor.known_self_slots.discard(my_slot)
                opponent.known_self_slots.discard(opp_slot)
            else:
                actor.known_self_slots.add(my_slot)
                actor.known_opp_cards[opp_slot] = opponent.hand[opp_slot]
                opponent.known_self_slots.discard(opp_slot)

        else:
            raise ValueError(f"Unhandled power action kind: {kind}")

        self.state.drawn_card = None
        self._advance_turn()

    def _advance_turn(self) -> None:
        assert self.state is not None
        just_finished = self.state.current_player
        self.state.current_player = 1 - self.state.current_player
        self.state.phase = "start_turn"
        self.state.turn_count += 1
        self.state.drawn_card = None

        if self.state.cambio_called_by is None:
            return

        if just_finished == self.state.cambio_called_by:
            return

        if self.state.final_turns_remaining is None:
            return

        self.state.final_turns_remaining -= 1
        if self.state.final_turns_remaining <= 0:
            self.state.done = True