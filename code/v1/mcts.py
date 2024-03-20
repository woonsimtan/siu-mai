import numpy as np
from collections import defaultdict
import pdb


class MonteCarloTreeSearchNode:
    def __init__(self, state, simulations, parent=None, parent_action=None):
        self.simulations = simulations
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = 0
        # self._results = defaultdict(int)
        # self._results[1] = 0
        # self._results[-1] = 0
        self._untried_actions = self.untried_actions()
        self.maximising_player = state._current_player_number
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        # wins = self._results[1]
        # loses = self._results[-1]
        # q_value = wins - loses
        # return q_value
        return self._results

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, self.simulations, parent=self, parent_action=action
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
        self._number_of_visits += 1.0
        # self._results[result] += 1.0
        self._results += result

        if self.parent is not None:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [
            (c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]

        if len(choices_weights) == 0:
            return -1

        # if there are same values, return random child
        indices = [
            i for i, x in enumerate(choices_weights) if x == max(choices_weights)
        ]
        if len(indices) > 1:
            return self.children[np.random.choice(indices)]
        else:
            return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        for i in range(self.simulations):
            # limit_count = self.completed_games * 10
            # i = 0
            # while self._results[1] + self._results[-1] < self.completed_games and i < limit_count:
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
            i += 1

        return self.best_child(c_param=0.0)  # value can (and should) be adjusted

    # def get_legal_actions(self):
    #     actions = []
    #     p = self.state._current_player_number
    #     if self.state._players[p].get_hidden_tiles().size() % 3 == 2:
    #         for tile in self.state._players[p].get_hidden_tiles().tiles:
    #             actions.append(["DISCARD", tile])
    #     else:
    #         if self.state.any_peng() != -1:
    #             actions.append(["PENG"])
    #         actions.append(["PICKUP"])

    #     return actions

    def is_game_over(self):
        return self.state.ended()

    def move(self, action):
        return self.state.next_game_state(action)
