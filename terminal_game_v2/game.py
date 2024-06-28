import random
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import pygame
import json
import socket
import threading

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock, Paper, Scissors Game")
        self.score = {"player1": 0, "player2": 0, "ties": 0}
        self.high_scores = []
        self.leaderboard = []
        self.game_log = []
        self.player1_name = ""
        self.player2_name = "Computer"
        self.rounds = 0
        self.sound_on = True
        self.difficulty = "easy"
        self.player_stats = {"player1": {"wins": 0, "losses": 0, "ties": 0}, "player2": {"wins": 0, "losses": 0, "ties": 0}}
        self.achievements = {"First Win": False, "First Tie": False, "Win Streak 3": False, "Loss Streak 3": False}
        self.theme = "Light"
        self.timer_seconds = 10
        self.timer_running = False

        pygame.mixer.init()
        self.win_sound = pygame.mixer.Sound("win.wav")
        self.lose_sound = pygame.mixer.Sound("lose.wav")
        self.tie_sound = pygame.mixer.Sound("tie.wav")

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Save Game", command=self.save_game)
        game_menu.add_command(label="Load Game", command=self.load_game)
        game_menu.add_command(label="Reset Leaderboard", command=self.reset_leaderboard)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Toggle Sound", command=self.toggle_sound)
        options_menu.add_command(label="Change Difficulty", command=self.change_difficulty)
        options_menu.add_command(label="User Settings", command=self.user_settings)
        options_menu.add_command(label="Change Theme", command=self.change_theme)

        network_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Network", menu=network_menu)
        network_menu.add_command(label="Host Game", command=self.host_game)
        network_menu.add_command(label="Join Game", command=self.join_game)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Welcome to Rock, Paper, Scissors!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.choice_var = tk.StringVar(value="rock")
        self.rock_button = tk.Radiobutton(self.root, text="Rock", variable=self.choice_var, value="rock")
        self.paper_button = tk.Radiobutton(self.root, text="Paper", variable=self.choice_var, value="paper")
        self.scissors_button = tk.Radiobutton(self.root, text="Scissors", variable=self.choice_var, value="scissors")
        self.rock_button.pack()
        self.paper_button.pack()
        self.scissors_button.pack()

        self.play_button = tk.Button(self.root, text="Play", command=self.play_round)
        self.play_button.pack(pady=20)

        self.score_label = tk.Label(self.root, text="Score - Wins: 0, Losses: 0, Ties: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=20)

        self.high_score_button = tk.Button(self.root, text="Show High Scores", command=self.show_high_scores)
        self.high_score_button.pack(pady=20)

        self.leaderboard_button = tk.Button(self.root, text="Show Leaderboard", command=self.show_leaderboard)
        self.leaderboard_button.pack(pady=20)

        self.log_button = tk.Button(self.root, text="Show Game Log", command=self.show_game_log)
        self.log_button.pack(pady=20)

        self.stats_button = tk.Button(self.root, text="Show Player Statistics", command=self.show_statistics)
        self.stats_button.pack(pady=20)

        self.achievements_button = tk.Button(self.root, text="Show Achievements", command=self.show_achievements)
        self.achievements_button.pack(pady=20)

        self.timer_label = tk.Label(self.root, text="Time Left: 10 seconds", font=("Helvetica", 14))
        self.timer_label.pack(pady=20)

    def new_game(self):
        self.player1_name = simpledialog.askstring("Player 1 Name", "Enter name for Player 1:")
        game_mode = simpledialog.askinteger("Game Mode", "Choose game mode:\n1 for single player\n2 for two players\n3 for network game")
        if game_mode == 2:
            self.player2_name = simpledialog.askstring("Player 2 Name", "Enter name for Player 2:")
        elif game_mode == 3:
            self.player2_name = "Network Player"
            self.host_game()  # Automatically host a game for network mode
        else:
            self.player2_name = "Computer"

        self.rounds = simpledialog.askinteger("Rounds", "Choose number of rounds (3, 5, 7):")
        self.score = {"player1": 0, "player2": 0, "ties": 0}
        self.game_log = []
        self.update_score_label()

    def play_round(self):
        if not self.player1_name:
            messagebox.showwarning("No Game", "Please start a new game from the menu.")
            return

        player1_choice = self.choice_var.get()
        if self.player2_name == "Computer":
            player2_choice = self.computer_choice()
        elif self.player2_name == "Network Player":
            player2_choice = self.network_player_choice()  # Method to get choice from network player
        else:
            player2_choice = simpledialog.askstring("Player 2 Choice", f"{self.player2_name}, choose: rock, paper, or scissors:")

        if player2_choice not in ["rock", "paper", "scissors"]:
            messagebox.showwarning("Invalid Choice", "Invalid choice for Player 2.")
            return

        self.animate_choices(player1_choice, player2_choice)
        result = self.determine_winner(player1_choice, player2_choice)
        if result == "tie":
            self.score["ties"] += 1
            self.check_achievements("tie")
            if self.sound_on:
                self.tie_sound.play()
        elif result == "player1":
            self.score["player1"] += 1
            self.player_stats["player1"]["wins"] += 1
            self.player_stats["player2"]["losses"] += 1
            self.check_achievements("player1")
            if self.sound_on:
                self.win_sound.play()
        else:
            self.score["player2"] += 1
            self.player_stats["player2"]["wins"] += 1
            self.player_stats["player1"]["losses"] += 1
            self.check_achievements("player2")
            if self.sound_on:
                self.lose_sound.play()

        self.player_stats["player1"]["ties"] = self.score["ties"]
        self.player_stats["player2"]["ties"] = self.score["ties"]

        self.game_log.append(f"Round {len(self.game_log) + 1}: {self.player1_name} chose {player1_choice}, {self.player2_name} chose {player2_choice} - {result.upper()}!")
        self.update_score_label()

        if self.score["player1"] > self.rounds // 2 or self.score["player2"] > self.rounds // 2:
            self.end_game()

    def computer_choice(self):
        if self.difficulty == "easy":
            return random.choice(["rock", "paper", "scissors"])
        elif self.difficulty == "medium":
            return random.choices(["rock", "paper", "scissors"], weights=[3, 3, 2])[0]
        elif self.difficulty == "hard":
            # Example advanced AI strategy: favor the choice that beats the player's previous choice
            if len(self.game_log) > 0:
                last_player_choice = self.game_log[-1].split()[4]
                if last_player_choice == "rock":
                    return "paper"
                elif last_player_choice == "paper":
                    return "scissors"
                else:
                    return "rock"
            else:
                return random.choice(["rock", "paper", "scissors"])

    def determine_winner(self, player1_choice, player2_choice):
        if player1_choice == player2_choice:
            return "tie"
        elif (player1_choice == "rock" and player2_choice == "scissors") or \
             (player1_choice == "scissors" and player2_choice == "paper") or \
             (player1_choice == "paper" and player2_choice == "rock"):
            return "player1"
        else:
            return "player2"

    def update_score_label(self):
        self.score_label.config(text=f"Score - {self.player1_name}: {self.score['player1']}, {self.player2_name}: {self.score['player2']}, Ties: {self.score['ties']}")

    def end_game(self):
        winner = self.player1_name if self.score["player1"] > self.score["player2"] else self.player2_name
        messagebox.showinfo("Game Over", f"Game over! {winner} wins!")
        self.save_high_score(winner)
        self.new_game()

    def save_high_score(self, winner):
        self.high_scores.append({"player1": self.player1_name, "player2": self.player2_name, "winner": winner, "score": self.score})
        self.high_scores = sorted(self.high_scores, key=lambda x: (x["score"]["player1"], x["score"]["player2"]), reverse=True)[:5]

        self.leaderboard.append({"player": winner, "wins": self.score["player1"], "losses": self.score["player2"], "ties": self.score["ties"]})
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x["wins"], reverse=True)[:5]

    def check_achievements(self, result):
        if result == "player1":
            if self.score["player1"] == 1 and not self.achievements["First Win"]:
                self.achievements["First Win"] = True
                messagebox.showinfo("Achievement Unlocked", "Achievement Unlocked: First Win!")
            if self.score["player1"] >= 3 and not self.achievements["Win Streak 3"]:
                self.achievements["Win Streak 3"] = True
                messagebox.showinfo("Achievement Unlocked", "Achievement Unlocked: Win Streak 3!")
        elif result == "tie":
            if self.score["ties"] == 1 and not self.achievements["First Tie"]:
                self.achievements["First Tie"] = True
                messagebox.showinfo("Achievement Unlocked", "Achievement Unlocked: First Tie!")
        elif result == "player2":
            if self.score["player2"] >= 3 and not self.achievements["Loss Streak 3"]:
                self.achievements["Loss Streak 3"] = True
                messagebox.showinfo("Achievement Unlocked", "Achievement Unlocked: Loss Streak 3!")

    def show_achievements(self):
        achievements_text = "Achievements:\n"
        for achievement, unlocked in self.achievements.items():
            status = "Unlocked" if unlocked else "Locked"
            achievements_text += f"{achievement}: {status}\n"
        messagebox.showinfo("Achievements", achievements_text)

    def save_game(self):
        game_data = {
            "score": self.score,
            "high_scores": self.high_scores,
            "leaderboard": self.leaderboard,
            "game_log": self.game_log,
            "player1_name": self.player1_name,
            "player2_name": self.player2_name,
            "rounds": self.rounds,
            "difficulty": self.difficulty,
            "player_stats": self.player_stats,
            "sound_on": self.sound_on,
            "achievements": self.achievements,
            "theme": self.theme,
            "timer_seconds": self.timer_seconds,
            "timer_running": self.timer_running
        }
        with open("game_save.json", "w") as file:
            json.dump(game_data, file)
        messagebox.showinfo("Game Saved", "Game has been saved successfully.")

    def load_game(self):
        try:
            with open("game_save.json", "r") as file:
                game_data = json.load(file)
            self.score = game_data["score"]
            self.high_scores = game_data["high_scores"]
            self.leaderboard = game_data["leaderboard"]
            self.game_log = game_data["game_log"]
            self.player1_name = game_data["player1_name"]
            self.player2_name = game_data["player2_name"]
            self.rounds = game_data["rounds"]
            self.difficulty = game_data["difficulty"]
            self.player_stats = game_data["player_stats"]
            self.sound_on = game_data["sound_on"]
            self.achievements = game_data["achievements"]
            self.theme = game_data["theme"]
            self.timer_seconds = game_data["timer_seconds"]
            self.timer_running = game_data["timer_running"]
            self.update_score_label()
            messagebox.showinfo("Game Loaded", "Game has been loaded successfully.")
        except FileNotFoundError:
            messagebox.showwarning("Load Failed", "No saved game found.")

    def reset_leaderboard(self):
        self.leaderboard = []
        messagebox.showinfo("Reset Leaderboard", "Leaderboard has been reset.")

    def show_high_scores(self):
        high_score_text = "High Scores:\n"
        for hs in self.high_scores:
            high_score_text += f"{hs['player1']} vs {hs['player2']} - Winner: {hs['winner']} - Score: {hs['score']['player1']}:{hs['score']['player2']}\n"
        messagebox.showinfo("High Scores", high_score_text)

    def show_leaderboard(self):
        leaderboard_text = "Leaderboard:\n"
        for lb in self.leaderboard:
            leaderboard_text += f"Player: {lb['player']} - Wins: {lb['wins']}, Losses: {lb['losses']}, Ties: {lb['ties']}\n"
        messagebox.showinfo("Leaderboard", leaderboard_text)

    def show_game_log(self):
        log_text = "Game Log:\n"
        for entry in self.game_log:
            log_text += entry + "\n"
        messagebox.showinfo("Game Log", log_text)

    def show_statistics(self):
        stats_text = "Player Statistics:\n"
        stats_text += f"{self.player1_name} - Wins: {self.player_stats['player1']['wins']}, Losses: {self.player_stats['player1']['losses']}, Ties: {self.player_stats['player1']['ties']}\n"
        stats_text += f"{self.player2_name} - Wins: {self.player_stats['player2']['wins']}, Losses: {self.player_stats['player2']['losses']}, Ties: {self.player_stats['player2']['ties']}\n"
        messagebox.showinfo("Player Statistics", stats_text)

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        status = "on" if self.sound_on else "off"
        messagebox.showinfo("Toggle Sound", f"Sound has been turned {status}.")

    def change_difficulty(self):
        self.difficulty = simpledialog.askstring("Change Difficulty", "Choose difficulty level (easy, medium, hard):")
        if self.difficulty not in ["easy", "medium", "hard"]:
            self.difficulty = "easy"
            messagebox.showwarning("Invalid Difficulty", "Invalid difficulty level. Setting to easy.")

    def user_settings(self):
        self.player1_name = simpledialog.askstring("Player 1 Name", "Enter name for Player 1:", initialvalue=self.player1_name)
        self.player2_name = simpledialog.askstring("Player 2 Name", "Enter name for Player 2:", initialvalue=self.player2_name)

    def change_theme(self):
        self.theme = simpledialog.askstring("Change Theme", "Choose theme (Light, Dark):")
        if self.theme not in ["Light", "Dark"]:
            self.theme = "Light"
            messagebox.showwarning("Invalid Theme", "Invalid theme. Setting to Light.")
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "Light":
            self.root.config(bg="white")
            self.label.config(bg="white", fg="black")
            self.score_label.config(bg="white", fg="black")
            self.timer_label.config(bg="white", fg="black")
        else:
            self.root.config(bg="black")
            self.label.config(bg="black", fg="white")
            self.score_label.config(bg="black", fg="white")
            self.timer_label.config(bg="black", fg="white")

    def start_timer(self):
        self.timer_running = True
        self.timer_seconds = 10
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.timer_seconds -= 1
            self.timer_label.config(text=f"Time Left: {self.timer_seconds} seconds")
            if self.timer_seconds <= 0:
                self.timer_running = False
                self.play_round()
            else:
                self.root.after(1000, self.update_timer)

    def host_game(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 12345))
        self.server.listen(1)
        threading.Thread(target=self.accept_connection).start()
        messagebox.showinfo("Host Game", "Hosting game on port 12345. Waiting for players to join...")

    def accept_connection(self):
        self.connection, addr = self.server.accept()
        messagebox.showinfo("Player Joined", f"Player joined from {addr}")
        threading.Thread(target=self.receive_data).start()

    def join_game(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = simpledialog.askstring("Join Game", "Enter host IP address:")
        self.connection.connect((host, 12345))
        threading.Thread(target=self.receive_data).start()
        messagebox.showinfo("Join Game", "Joined game successfully.")

    def send_data(self, data):
        self.connection.sendall(data.encode('utf-8'))

    def receive_data(self):
        while True:
            data = self.connection.recv(1024).decode('utf-8')
            if data:
                self.handle_network_data(data)

    def handle_network_data(self, data):
        if data.startswith("choice:"):
            self.network_player_choice = data.split(":")[1]

    def network_player_choice(self):
        self.send_data(f"choice:{self.choice_var.get()}")
        return self.network_player_choice

    def show_about(self):
        messagebox.showinfo("About", "Rock, Paper, Scissors Game\nVersion 1.0\nDeveloped by OpenAI")

    def animate_choices(self, player1_choice, player2_choice):
        animation_text = f"{self.player1_name} chose {player1_choice}, {self.player2_name} chose {player2_choice}"
        self.label.config(text=animation_text)
        self.root.update()
        time.sleep(1)  # Add delay to show choices before displaying result

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
