import numpy as np

class MDP:
    def __init__(self, N):
        self.N = N  # NxN board size
        self.states = set()
        self.T_states = set()
        self.actions = {}

    def generate_states(self):
        """
        Generates all possible states of the game for an NxN board.
        """
        def _brute_states():
            """
            Generates all possible states for the board.
            """
            # 0: no move, 1: X, 2: O
            all_board_config = set()
            for values in np.ndindex(*([3] * (self.N ** 2))):
                state = tuple(values)
                all_board_config.add(state)
            return all_board_config

        def _check_2_win(state):
            """
            Checks if there are two winners at the same time.
            """
            count_h, count_v = 0, 0
            for i in range(self.N):
                # Check rows for winner
                if len(set(state[i*self.N:(i+1)*self.N])) == 1 and state[i*self.N] in {1, 2}:
                    count_h += 1
                # Check columns for winner
                if len(set(state[i::self.N])) == 1 and state[i] in {1, 2}:
                    count_v += 1
            if count_h == 2 or count_v == 2:
                return True
            return False

        self.states = _brute_states()
        
        # Filter out invalid states
        for state in self.states.copy():
            if state.count(1) > state.count(2):
                self.states.remove(state)
            elif abs(state.count(1) - state.count(2)) > 1:
                self.states.remove(state)
            elif _check_2_win(state):
                self.states.remove(state)

    def termination_states(self):
        """
        Updates terminal states where the game is over (win, draw, loss).
        """
        for state in self.states:
            if self.win(state):
                self.T_states.add(state)
            elif state.count(0) == 0:  # All spots are filled, it's a draw
                self.T_states.add(state)

    def generate_actions(self):
        """
        Updates the possible actions for each state.
        """
        for state in self.states:
            self.actions[state] = None
            if state not in self.T_states:
                self.actions[state] = []
                for i in range(self.N ** 2):
                    if state[i] == 0:
                        self.actions[state].append(i)

    def transition_function(self, state):
        """
        Returns the probability of each possible next state.
        """
        if state in self.T_states:
            return 0
        else:
            return 1 / (len(self.actions[state]) - 1)

    def reward_function(self, state):
        """
        Returns the reward for the given state.
        """
        if self.win(state) == 1:
            return 1
        if self.win(state) == 2:
            return -1
        return 0

    def win(self, state):
        """
        Checks if a player has won the game.
        """
        # Check rows and columns
        for i in range(self.N):
            # Check rows
            if len(set(state[i*self.N:(i+1)*self.N])) == 1 and state[i*self.N] != 0:
                return state[i*self.N]
            # Check columns
            if len(set(state[i::self.N])) == 1 and state[i] != 0:
                return state[i]
        # Check diagonals
        if len(set([state[i*(self.N+1)] for i in range(self.N)])) == 1 and state[0] != 0:
            return state[0]
        if len(set([state[(i+1)*(self.N-1)] for i in range(self.N)])) == 1 and state[self.N-1] != 0:
            return state[self.N-1]
        return False

    def possible_next_states(self, state, action):
        """
        Returns the possible next states given a current state and action.
        """
        new_state = list(state)
        new_state[action] = 1
        if self.win(new_state):
            return []
        possible_next_states = []
        for i, case in enumerate(new_state):
            next_new_state = new_state.copy()
            if case == 0:
                next_new_state[i] = 2
                possible_next_states.append(tuple(next_new_state))
        return possible_next_states
