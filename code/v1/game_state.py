from v1.tiles import *


class GameState:
    def __init__(
        self, deck, players, discarded_tiles, last_discarded, current_player_number
    ):
        self._deck = deck
        self._players = players
        self._discarded_tiles = discarded_tiles.copy()
        self._last_discarded = last_discarded.copy()
        self._current_player_number = current_player_number

    @property
    def deck(self):
        return self._deck.copy()

    @property
    def discarded_tiles(self):
        return self._discarded_tiles.copy()

    def get_tiles_hidden_from_player(self):
        """
        Returns a TileList of all tiles that are hidden from the current player
        """
        hidden_tiles = self.deck
        for i in range(4):
            if i != self._current_player_number:
                hidden_tiles.add_tiles(self._players.get_hidden_tiles())
        return hidden_tiles

    def update_game_state(self, action):
        """
        Returns a new game state after the action has been taken
        """
        pass
