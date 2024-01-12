from v1.tiles import *
from copy import deepcopy


class GameState:
    def __init__(
        self,
        deck,
        players,
        discarded_tiles=TileList([]),
        last_discarded=DUMMY_TILE,
        current_player_number=0,
    ):
        self._deck = deck
        self._players = players.copy()
        self._discarded_tiles = discarded_tiles.copy()
        self._last_discarded = last_discarded.copy()
        self._current_player_number = current_player_number

    def print(self):
        print("--- Game State ---")
        for i in range(4):
            print(f"Player {i}:")
            self._players[i].all_tiles().print()
        print("Last discarded:", self._last_discarded.to_string())
        print(f"Current player: {self._current_player_number}")

    @property
    def deck(self):
        return self._deck.copy()

    @property
    def discarded_tiles(self):
        return self._discarded_tiles.copy()

    def any_peng(self):
        for i in range(4):
            p = self._players[i]
            if p.check_for_peng(self._last_discarded):
                if self._current_player_number != i:
                    return i
        return -1

    def any_wins(self, discarded):
        try:
            for i in range(4):
                p = self._players[i]
                if p.check_for_win(discarded):
                    return i
            return -1
        except ValueError:
            p.all_tiles().print()
            raise ValueError(
                f"Player {i} has invalid number of tiles: {p.all_tiles().size()}"
            )

    def ended(self):
        if self.deck.size() == 0:
            return True
        for p in self._players:
            if p.check_for_win(self._last_discarded):
                return True
        return False

    def get_legal_actions(self):
        actions = []
        p = self._current_player_number
        if self._players[p].get_hidden_tiles().size() % 3 == 2:
            for tile in self._players[p].get_hidden_tiles().tiles:
                actions.append(["DISCARD", tile])
        else:
            if self.any_peng() != -1:
                actions.append(["PENG"])  # and "PASS"
            actions.append(["PICKUP"])

        return actions

    # def get_next_action(self):
    #     # check for peng
    #     peng_player = self.any_peng()
    #     if peng_player != -1:
    #         p = self._players[peng_player]
    #         if p.choose_peng():
    #             return "PENG"
    #     # else next player picks up
    #     return "PICKUP"

    def get_tiles_hidden_from_player(self):
        """
        Returns a TileList of all tiles that are hidden from the current player
        """
        hidden_tiles = self.deck
        for i in range(4):
            if i != self._current_player_number:
                hidden_tiles.add_tiles(self._players.get_hidden_tiles())
        return hidden_tiles

    def next_game_state(self):
        """
        Returns a new game state after the action has been taken
        """
        # copy values
        deck = self._deck.copy()
        players = deepcopy(self._players)
        discarded_tiles = self._discarded_tiles.copy()
        last_discarded = self._last_discarded.copy()
        current_player_number = self._current_player_number
        game_end = False
        choose_peng = False

        # carry out actions
        if self.any_peng() != -1:
            choose_peng = players[self.any_peng()].choose_peng()
        if choose_peng:
            print("PENG")
            current_player_number = self.any_peng()
            players[current_player_number].peng(last_discarded)

        if not choose_peng:
            print("PICKUP")
            discarded_tiles.add(last_discarded)
            current_player_number = (current_player_number + 1) % 4
            players[current_player_number].pickup(deck.remove_random_tile())
            # check for win
            if players[current_player_number].check_for_win():
                last_discarded = DUMMY_TILE
                game_end = True

        # discard
        if not game_end:
            print("DISCARD")
            if players[current_player_number].is_mcts():
                last_discarded = players[current_player_number].discard(self)
            else:
                last_discarded = players[current_player_number].discard()

        # return new game state
        return GameState(
            deck,
            players,
            discarded_tiles,
            last_discarded,
            current_player_number,
        )
