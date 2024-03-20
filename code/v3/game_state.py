from v3.tiles import *
from copy import deepcopy
from v3.players import *
import pdb
from typing import List, Tuple


class GameState:
    def __init__(
        self,
        deck: TileList,
        players: List[Player],
        discarded_tiles: TileList = TileList([]),
        last_discarded: Tile = DUMMY_TILE,
        current_player_number: int = 3,
        exhausted_tiles=TileList([]),
    ):
        self._deck = deck
        self._players = players.copy()
        self._discarded_tiles = discarded_tiles.copy()
        self._last_discarded = last_discarded.copy()
        self._current_player_number = current_player_number
        self._exhausted_tiles = exhausted_tiles.copy()

    def print(self) -> None:
        """
        Prints all the tiles of each player and the last discarded tile.
        """
        print("--- Game State ---")
        for i in range(4):
            print(f"Player {i}:")
            self._players[i].all_tiles().print()
        print("Last discarded:", self._last_discarded.to_string())
        print(f"Current player: {self._current_player_number}")

    @property
    def deck(self) -> TileList:
        return self._deck.copy()

    @property
    def discarded_tiles(self) -> TileList:
        return self._discarded_tiles.copy()

    def any_peng(self) -> int:
        """
        Checks if any player can PENG on the last discarded tile
        """
        for i in range(4):
            p = self._players[i]
            if p.check_for_peng(self._last_discarded):
                if self._current_player_number != i:
                    return i
        return -1

    def any_wins(self, discarded: Tile) -> int:
        """
        Checks if any player can win on the last discarded tile
        """
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

    def game_result(self, maximising_player: int) -> int:
        """
        Returns the score of the player to maximise, only used in MCTS
        """
        wins = [player.times_won for player in self._players]
        # if any player has won return the player's score
        if max(wins) > 0:
            return self._players[maximising_player].score
        # if no one has won there are 2 options
        # option 1: take hand score relative to the other players
        else:
            scores = [p.all_tiles().hand_score(p.unwanted_suit) for p in self._players]
            max_player_score = scores.pop(maximising_player)
            # a) take the highest of other player's score
            other_score = max(scores)
            # # b) take the average of the other player's score
            # other_score = sum(scores) / len(scores)
            return max_player_score - other_score
        # # option 2: return a neutral result
        # # (but this reduces the difference between weights of choices)
        # else:
        #     return 0

    def ended(self) -> bool:
        """
        Returns if the game has ended
        """
        if self.deck.size() == 0:
            return True
        return False

    def get_legal_actions(self) -> List:
        """
        Returns a list of possible actions that could fold out from the current game state.
        """
        actions = []
        p = self._current_player_number
        if self._players[p].get_hidden_tiles().size() % 3 == 2:
            for tile in self._players[p].possible_discards.tiles:
                actions.append(["DISCARD", tile])
        else:
            if self.any_peng() == p:
                actions.append(["PENG"])
                actions.append(["PASS"])
            else:
                actions.append(["PICKUP"])
        return actions

    def initialise_mcts_state(self):
        """
        Initialises a new game state for the MCTS algorithm
        """
        # get all tiles hidden from player
        hidden_tiles = self.get_tiles_hidden_from_player()

        # reassign tiles
        players = [0, 0, 0, 0]
        # for current player initialise as a SemiRandomAgent with the same tiles
        players[self._current_player_number] = SemiRandomAgent(
            self._players[self._current_player_number].get_hidden_tiles(),
            self._players[self._current_player_number].displayed_tiles,
            self._players[self._current_player_number].unwanted_suit,
            last_discarded=self._players[self._current_player_number].last_discarded,
        )

        for i in range(4):
            if i != self._current_player_number:
                # guess the tiles of the players who have discarded tiles not of their unwanted suit
                # (they have no tiles of their unwanted suit in their hand)
                if (
                    self._players[i].last_discarded.suit_type
                    != self._players[i].unwanted_suit
                ):
                    newly_assigned_tiles = TileList([])

                    hidden_subset = TileList(
                        [
                            tile
                            for tile in hidden_tiles.tiles
                            if tile.suit_type != self._players[i].unwanted_suit
                        ]
                    )

                    for j in range(
                        min(
                            self._players[i].get_hidden_tiles().size(),
                            hidden_subset.size(),
                        )
                    ):
                        newly_assigned_tiles.add(hidden_subset.remove_random_tile())

                    # remove these tiles from hidden
                    hidden_tiles.remove_tiles(newly_assigned_tiles)

                    # if there are any issues default to blindly guessing
                    for j in range(
                        self._players[i].get_hidden_tiles().size()
                        - newly_assigned_tiles.size()
                    ):
                        newly_assigned_tiles.add(hidden_tiles.remove_random_tile())

                    players[i] = SemiRandomAgent(
                        newly_assigned_tiles,
                        self._players[i].displayed_tiles,
                        self._players[i].unwanted_suit,
                        last_discarded=self._players[i].last_discarded,
                    )

        for i in range(4):
            if i != self._current_player_number:
                # guess the tiles of the players who have discarded tiles not of their unwanted suit
                # (they have no tiles of their unwanted suit in their hand)
                if (
                    self._players[i].last_discarded.suit_type
                    == self._players[i].unwanted_suit
                ):
                    newly_assigned_tiles = TileList([])

                    for j in range(self._players[i].get_hidden_tiles().size()):
                        newly_assigned_tiles.add(hidden_tiles.remove_random_tile())

                    players[i] = SemiRandomAgent(
                        newly_assigned_tiles,
                        self._players[i].displayed_tiles,
                        self._players[i].unwanted_suit,
                        last_discarded=self._players[i].last_discarded,
                    )

        return GameState(
            hidden_tiles,
            players,
            self._discarded_tiles,
            self._last_discarded,
            self._current_player_number,
            self._exhausted_tiles,
        )

    def get_tiles_hidden_from_player(self) -> TileList:
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
        players = [deepcopy(player) for player in self._players]
        discarded_tiles = self._discarded_tiles.copy()
        last_discarded = self._last_discarded.copy()
        current_player_number = self._current_player_number
        no_discard = False
        choose_peng = False
        exhausted_tiles = self._exhausted_tiles.copy()

        # if a player can peng they should select if they carry out the action
        if self.any_peng() != -1:
            choose_peng = players[self.any_peng()].choose_peng()
        # player chooses to peng
        if (choose_peng and action is None) or (action == ["PENG"]):
            current_player_number = self.any_peng()
            players[current_player_number].peng(last_discarded)
        # otherwise next player picks up
        if (
            (self.any_peng() != -1 and not choose_peng)
            or (self.any_peng() == -1 and action is None)
            or (action == ["PICKUP"])
            or (action == ["PASS"])
        ):
            discarded_tiles.add(last_discarded)
            current_player_number = (current_player_number + 1) % 4
            pickup_tile = deck.remove_random_tile()

            # check for win from pickup tile
            if players[current_player_number].check_for_win(pickup_tile):
                last_discarded = DUMMY_TILE
                no_discard = True
                exhausted_tiles.add(pickup_tile)

                # update scores
                score = players[current_player_number].win_score(deck.size() == 0)
                for i in range(4):
                    if i != current_player_number:
                        players[i].score -= score
                    else:
                        players[i].score += score * 3

                # update player
                players[current_player_number].win()

            else:
                # add new tile to player's hand
                players[current_player_number].pickup(pickup_tile)

        # discard
        if (not no_discard and action is None) or (
            action is not None and action[0] == "DISCARD"
        ):
            if action is not None:
                last_discarded = players[current_player_number].discard(
                    specified_tile=action[1]
                )

            elif players[current_player_number].is_mcts():
                last_discarded = players[current_player_number].discard(
                    game_state=GameState(
                        deck,
                        players,
                        discarded_tiles,
                        last_discarded,
                        current_player_number,
                        exhausted_tiles,
                    )
                )
            else:
                last_discarded = players[current_player_number].discard()

        # check if any players win on discard tile and update scores accordingly
        win = self.any_wins(last_discarded)
        if win != -1 and not no_discard and win != current_player_number:
            score = players[win].win_score(deck.size() == 0, last_discarded)
            players[win].score += score
            players[current_player_number].score -= score
            players[win].win()

            exhausted_tiles.add(last_discarded)
            last_discarded = DUMMY_TILE
            current_player_number = win

        # check scores are valid
        scores = [p.score for p in players]
        if sum(scores) != 0:
            print(f"Scores: {scores}")
            raise ValueError("Scores do not sum to 0")

        # return new game state
        return GameState(
            deck,
            players,
            discarded_tiles,
            last_discarded,
            current_player_number,
            exhausted_tiles,
        )
