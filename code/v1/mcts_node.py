import numpy as np
from collections import defaultdict
from v1.tiles import TileList, Tile

# from v1.base_game import any_peng, any_wins

DUMMY_TILE = Tile("DUMMY", "TILE")


def any_peng(players, discarded):
    for i in range(4):
        p = players[i]
        if p.check_for_peng(discarded):
            return i
    return -1


def any_wins(players, discarded):
    try:
        for i in range(4):
            p = players[i]
            if p.check_for_win(discarded):
                return i
        return -1
    except ValueError:
        p.print_all_tiles()
        raise ValueError(
            f"Player {i} has invalid number of tiles: {p.all_tiles().size()}"
        )


class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state  # player tiles, displayed_tiles, hidden tiles, discarded_tile, current_player, maximising_player
        self.parent = parent  # none for root node
        self.parent_action = (
            parent_action  # none for root node, action the parent just carried out
        )
        self.children = []  # all possible actions from current node
        self._number_of_visits = 0  # number of times current node is visited
        self._results = defaultdict(int)
        self._results[1] = 0  # wins
        self._results[-1] = 0  # losses
        # self._untried_actions = None  # list of untried actions
        # self._untried_actions = self.untried_actions()
        self._untried_actions = self.state.get_legal_actions()
        return

    # def untried_actions(self):
    #     self._untried_actions = self.state.get_legal_actions()
    #     return self._untried_actions

    def q(self):
        # difference of wins - losses
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        # print("Expanding")
        # From the present state, next state is generated depending on the action which is carried out.
        # In this step all the possible child nodes corresponding to generated
        # states are appended to the children array and the child_node is returned.
        # The states which are possible from the present state are all generated
        # and the child_node corresponding to this generated state is returned.
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action
        )

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        # print("checking terminal")
        return self.state.is_game_over()

    def rollout(self):
        """
        From the current state, entire game is simulated till there is an outcome for the game.
        This outcome of the game is returned. For example if it results in a win, the outcome is 1.
        Otherwise it is -1 if it results in a loss. And it is 0 if it is a tie.
        If the entire game is randomly simulated, that is at each turn the move is randomly selected out of set of possible moves,
        it is called light playout.
        """
        # print("rollout")
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            if len(possible_moves) == 0:
                print("Picking up no valid actions")
                print(current_rollout_state.is_game_over())
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        """
        In this step all the statistics for the nodes are updated.
        Until the parent node is reached, the number of visits for each node is incremented by 1.
        If the result is 1, that is it resulted in a win, then the win is incremented by 1.
        Otherwise if result is a loss, then loss is incremented by 1.
        """
        # print("backpropogate")
        self._number_of_visits += 1.0
        self._results[result] += 1.0
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        # print("checking fully expanded")
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        # print("best child")
        choices_weights = [
            (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        # print("tree policy called")
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        # print("best action")
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.0)


class GameState:
    def __init__(
        self,
        players,
        displayed_tiles,
        deck,
        discarded_tile,
        current_player,
        maximising_player,
    ):
        self.players = players
        self.displayed_tiles = displayed_tiles
        self.deck = deck
        self.discarded_tile = discarded_tile
        self.current_player = current_player
        self.maximising_player = maximising_player

    def get_hidden_tiles(self, player):
        all_hidden = self.deck.copy()
        for i in range(4):
            if i != player:
                # print(type(self.player_tiles[i]))
                all_hidden.add_tiles(self.players[i].get_hidden_tiles())
        return all_hidden

    def get_legal_actions(self):
        """
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        """
        actions = []

        last_discarded = self.discarded_tile
        # possible results: player i peng, player x+1 pickup, player x discard
        p = self.players[self.current_player]
        hidden = p.get_hidden_tiles()

        if hidden.size() % 3 == 2:
            for tile in p.get_possible_discards().tiles:
                actions.append(["DISCARD", tile])
        else:
            # pickup or peng
            if any_peng(self.players, last_discarded) != -1:
                actions.append(["PENG"])
            actions.append(["PICKUP"])

        # these cases are a winning hand but it's not being picked up on
        # if len(actions) == 0:
        #     p.get_hidden_tiles().print()
        #     p.get_possible_discards().print()
        #     print(last_discarded.to_string())
        #     print("No valid actions")
        return actions

    def is_game_over(self):
        """
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        """
        winning_player = any_wins(self.players, self.discarded_tile)
        game_over = (
            (winning_player != -1)
            or (self.deck.size() == 0)
            or (len(self.get_legal_actions()) == 0)
        )
        # if len(self.get_legal_actions()) == 0:
        #     print("No valid actions")
        #     print(game_over)
        #     print((winning_player != -1))
        #     print((self.deck.size() == 0))
        return game_over

    def game_result(self):
        """
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        """
        picked_up = False
        for p in self.players:
            picked_up = picked_up or p.get_hidden_tiles().size() % 3 == 2

        if picked_up:
            if self.players[self.current_player].check_for_win():
                winner = self.current_player
            else:
                return 0

        else:
            winner = any_wins(self.players, self.discarded_tile)

        if winner == self.maximising_player:
            return 1
        elif winner != -1:
            return -1
        else:
            return 0

    def move(self, action):
        """
        Modify according to your game or
        needs. Changes the state of your
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board
        position is empty. If you place x in
        row 2 column 3, then it would be some
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns
        the new state after making a move.
        """
        # print(action[0])
        # Case 1: PENG
        if action[0] == "PENG":
            # print("case 1")
            self.current_player = any_peng(self.players, self.discarded_tile)
            self.players[self.current_player].peng(self.discarded_tile)
            self.discarded_tile = DUMMY_TILE
        # Case 2: PICKUP
        elif action[0] == "PICKUP":
            # print("case 2")
            # needs to be shifted to legal moves
            pool = self.get_hidden_tiles(self.current_player)
            for k in range(4):
                if k != self.current_player:
                    pool.add_tiles(self.players[k].get_hidden_tiles())
            pickup_tile = pool.remove_random_tile()
            self.players[self.current_player].pickup(pickup_tile)
            self.discarded_tile = DUMMY_TILE
        # CASE 3:  DISCARD
        elif action[0] == "DISCARD":
            # print("case 3")
            self.discarded_tile = action[1]
            self.players[self.current_player].possible_discards.remove(action[1])
            self.current_player = (self.current_player + 1) % 4
        # print("moved")
        return self


# def mcts(initial_state):
#     root = MonteCarloTreeSearchNode(state=initial_state)
#     selected_node = root.best_action()
#     return selected_node
