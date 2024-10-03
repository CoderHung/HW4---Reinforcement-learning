import tkinter as tk
import tkinter.messagebox as messagebox
import random
import json
import matplotlib.pyplot as plt

class TicTacToeGUI:
    def __init__(self, agent="ValueIteration"):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = (0,) * 9
        self.buttons = [None] * 9
        self.is_vs_computer = False  # Flag to check if playing against the computer
        self.computer_symbol = "O"   # Symbol for the computer player
        self.agent = agent
        self.policy = {}
        path = "Policies/valueIteration.json"
        with open(path, 'r') as json_file:
            self.policy = json.load(json_file)

        # Center the window on the screen
        self.center_window()

        player_choice = tk.StringVar()
        player_choice.set("X")
        player_label = tk.Label(self.window, text="Choose your symbol:")
        player_label.grid(row=3, columnspan=3)
        x_radio = tk.Radiobutton(self.window, text="X", variable=player_choice, value="X")
        o_radio = tk.Radiobutton(self.window, text="O", variable=player_choice, value="O")
        x_radio.grid(row=4, column=0)
        o_radio.grid(row=4, column=1)

        # Checkbox for playing against the computer
        vs_computer_checkbox = tk.Checkbutton(self.window, text="Play vs Computer", command=self.toggle_vs_computer)
        vs_computer_checkbox.grid(row=5, columnspan=3)

        start_button = tk.Button(self.window, text="Start Game", command=lambda: self.start_game(player_choice.get()))
        start_button.grid(row=6, columnspan=3)

    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 320  # Adjust this as needed
        window_height = 430  # Adjust this as needed
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def toggle_vs_computer(self):
        self.is_vs_computer = not self.is_vs_computer

    def start_game(self, player_choice):
        self.computer_symbol = "O" if player_choice == "X" else "X"
        for i in range(9):
            button = tk.Button(self.window, text="", width=10, height=5, command=lambda idx=i: self.make_move(idx))
            button.grid(row=i // 3, column=i % 3)
            self.buttons[i] = button

        if self.computer_symbol == "X" and self.is_vs_computer:
            self.make_computer_move()

    def make_move(self, idx):
        if self.board[idx] == 0:
            self.board = self.board[:idx] + (1 if self.current_player == "X" else 2,) + self.board[idx + 1:]
            self.buttons[idx]['text'] = self.current_player
            if self.check_win() or self.check_tie():
                self.end_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.is_vs_computer and self.current_player == self.computer_symbol:
                    self.make_computer_move()

    def make_computer_move(self):
        state = self.board
        if self.computer_symbol == "O":
            state = tuple(3-x if x != 0 else 0 for x in state)
        self.make_move(self.policy[str(state)])

    def check_win(self):
        win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for combo in win_combinations:
            a, b, c = combo
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != 0:
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                return True
        return False

    def check_tie(self):
        if 0 not in self.board:
            messagebox.showinfo("Game Over", "It's a tie!")
            return True
        return False

    def end_game(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

        restart_button = tk.Button(self.window, text="Restart Game", command=self.restart_game)
        restart_button.grid(row=7, columnspan=3)

    def restart_game(self):
        self.window.destroy()
        self.__init__()
        self.start_game("X")

    def start(self):
        self.window.mainloop()

class TicTacToeAgent:
    def __init__(self, policy):
        self.policy = policy

    def choose_move(self, state):
        return self.policy.get(str(state), random.choice(self.get_available_moves(state)))

    def get_available_moves(self, state):
        return [i for i in range(9) if state[i] == 0]

class RandomAgent:
    def choose_move(self, state):
        return random.choice([i for i in range(9) if state[i] == 0])

def play_game(agent1, agent2):
    board = (0,) * 9
    current_agent = agent1
    while True:
        state = board
        move = current_agent.choose_move(state)
        board = board[:move] + (1 if current_agent == agent1 else 2,) + board[move + 1:]

        if check_win(board):
            return 1 if current_agent == agent1 else -1
        if check_tie(board):
            return 0
        current_agent = agent2 if current_agent == agent1 else agent1

def check_win(state):
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combo in win_combinations:
        a, b, c = combo
        if state[a] == state[b] == state[c] and state[a] != 0:
            return True
    return False

def check_tie(state):
    return 0 not in state

def simulate_games(num_games, policy):
    wins = 0
    draws = 0
    for _ in range(num_games):
        agent1 = TicTacToeAgent(policy)
        agent2 = RandomAgent()
        result = play_game(agent1, agent2)
        if result == 1:
            wins += 1
        elif result == 0:
            draws += 1
    return wins, draws

def plot_win_rate(num_games, wins, draws):
    win_rate = (wins / num_games) * 100
    draw_rate = (draws / num_games) * 100
    plt.bar(['Win Rate', 'Draw Rate'], [win_rate, draw_rate])
    plt.ylabel('Percentage')
    plt.title('Win Rate of Value Iteration Agent vs Random Agent')
    plt.ylim(0, 100)
    plt.show()

if __name__ == "__main__":
    num_games = 1000  # Set the number of games to simulate
    game = TicTacToeGUI("valueIteration")
    
    wins, draws = simulate_games(num_games, game.policy)
    plot_win_rate(num_games, wins, draws)
    
    game.start()

