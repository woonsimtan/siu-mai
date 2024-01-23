import numpy as np
from collections import defaultdict


class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = self.untried_actions()
        self.maximising_player = state._current_player_number
        return

    def untried_actions(self):
        # print("UNTRIED ACTIONS CALLED")
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        # print("EXPAND CALLED")
        action = self._untried_actions.pop()
        next_state = self.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.ended()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.ended():
            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.next_game_state(action)
        return current_rollout_state.game_result(self.maximising_player)

    def backpropagate(self, result):
        # print("BACKPROPOGATE CALLED")
        self._number_of_visits += 1.0
        self._results[result] += 1.0
        # print(self._results)
        if self.parent is not None:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        # print("BEST CHILD CALLED")
        choices_weights = [
            (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]
        if len(choices_weights) == 0:
            return -1
        # currently really likes to discard the tile it picked up? Don't understand why.

        # print(choices_weights)

        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        # print("ROLLOUT POLICY CALLED")
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        # print("TREE POLICY CALLED")
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        # print("BEST ACTION CALLED")
        simulation_no = 1000

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.0)

    def get_legal_actions(self):
        """
        Modify according to your game or
        needs. Constructs a list of all
        possible states from current state.
        Returns a list.
        """
        actions = []
        p = self.state._current_player_number
        if self.state._players[p].get_hidden_tiles().size() % 3 == 2:
            for tile in self.state._players[p].get_hidden_tiles().tiles:
                actions.append(["DISCARD", tile])
        else:
            if self.state.any_peng() != -1:
                actions.append(["PENG"])
            actions.append(["PICKUP"])

        return actions

    def is_game_over(self):
        """
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        """
        return self.state.ended()

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
        return self.state.next_game_state(action)
