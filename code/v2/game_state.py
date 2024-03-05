from tiles import *
from copy import deepcopy
from players import SemiRandomAgent
import pdb


class GameState:
    def __init__(
        self,
        deck,
        players,
        discarded_tiles=TileList([]),
        last_discarded=DUMMY_TILE,
        current_player_number=3,
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

    def game_result(self, maximising_player):

        # if self.any_wins(DUMMY_TILE) == maximising_player:
        #     return self._players[maximising_player].win_score(self.deck.size() == 0)
        # elif self.any_wins(DUMMY_TILE) != -1:
        #     return - self._players[self.any_wins(DUMMY_TILE)].win_score(self.deck.size() == 0)

        if self.any_wins(self._last_discarded) == maximising_player:
            return self._players[maximising_player].win_score(self.deck.size() == 0)
        elif self.any_wins(self._last_discarded) != -1:
            return - self._players[self.any_wins(self._last_discarded)].win_score(self.deck.size() == 0)
        # for win scoring, if no one has won: 
        # option 1: take hand score
        else:
            scores = [p.all_tiles().hand_score(p.unwanted_suit) for p in self._players]
            max_player_score = scores.pop(maximising_player)
            # option 1: take the highest of other player's score
            other_score = max(scores)
            # # option 2: take the average of the other player's score
            # other_score = sum(scores) / len(scores)
            return max_player_score - other_score
        # # option 2: result = 0
        # # weights are too much just 0
        # else:
        #     return 0

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
            if self.any_peng() == p:
                actions.append(["PENG"])
                actions.append(["PASS"]) 
            else:
                actions.append(["PICKUP"])
        return actions

    def initialise_mcts_state(self):
        hidden_tiles = self.get_tiles_hidden_from_player()

        # reassign tiles
        players = []
        for i in range(4):
            if i == self._current_player_number:
                players.append(
                    SemiRandomAgent(
                        self._players[i].possible_discards,
                        self._players[i].displayed_tiles,
                        self._players[i].unwanted_suit
                    )
                )
            else:
                newly_assigned_tiles = TileList([])
                for j in range(self._players[i].possible_discards.size()):
                    newly_assigned_tiles.add(hidden_tiles.remove_random_tile())
                players.append(
                    SemiRandomAgent(
                        newly_assigned_tiles,
                        self._players[i].displayed_tiles,
                        self._players[i].unwanted_suit,
                    )
                )

        return GameState(
            hidden_tiles,
            players,
            self._discarded_tiles,
            self._last_discarded,
            self._current_player_number,
        )

    def get_tiles_hidden_from_player(self):
        """
        Returns a TileList of all tiles that are hidden from the current player
        """
        hidden_tiles = self.deck
        for i in range(4):
            if i != self._current_player_number:
                hidden_tiles.add_tiles(self._players[i].get_hidden_tiles())
        return hidden_tiles

    def next_game_state(self, action=None):
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
        # if a player can peng they should select if they carry out the action
        if self.any_peng() != -1:
            choose_peng = players[self.any_peng()].choose_peng()
        # player chooses to peng
        if (choose_peng and action is None) or (action == ["PENG"]):
            current_player_number = self.any_peng()
            players[current_player_number].peng(last_discarded)
        # TODO: check these conditions (no peng occurs)
        if (
            (self.any_peng() != -1 and not choose_peng)
            or (self.any_peng() == -1 and action is None)
            or (action == ["PICKUP"])
            or (action == ["PASS"])
        ):
            discarded_tiles.add(last_discarded)
            current_player_number = (current_player_number + 1) % 4
            players[current_player_number].pickup(deck.remove_random_tile())
            # check for win from pickup tile
            if players[current_player_number].check_for_win():
                last_discarded = DUMMY_TILE
                game_end = True

        # discard
        if (not game_end and action is None) or (
            action is not None and action[0] == "DISCARD"
        ):
            if players[current_player_number].is_mcts():
                last_discarded = players[current_player_number].discard(
                    GameState(
                        deck,
                        players,
                        discarded_tiles,
                        last_discarded,
                        current_player_number,
                    )
                )
            else:
                last_discarded = players[current_player_number].discard()

        players_copy = []
        for i in range(4):
            if i == current_player_number:
                players_copy.append(players[i])
            else:
                players_copy.append(self._players[i])

        # check for invalid number of tiles
        for p in players_copy:
            if (not game_end and p.all_tiles().size() != 13):
                p.all_tiles().print()
                raise ValueError(f"Player {players_copy.index(p)} has invalid number of tiles: {p.all_tiles().size()}")

        # return new game state
        return GameState(
            deck,
            players_copy,  
            # why does this instead of players mean that there isn't a problem of the peng being added to the wrong player?
            # does it mean actually it's still adding peng to the wrong player?
            # and i'm not seeing it because i'm doing this step?
            # is that why players end up with unwanted suit in their displayed/locked tiles?
            discarded_tiles,
            last_discarded,
            current_player_number,
        )
