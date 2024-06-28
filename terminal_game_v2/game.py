import random
import time
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
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
        self.player1_name = ""
        self.player2_name = "Computer"
        self.rounds = 0
        self.difficulty = "easy"
        self.player_stats = {"player1": {"wins": 0, "losses": 0, "ties": 0},
                             "player2": {"wins": 0, "losses": 0, "ties": 0}}
        self.sound_on = True
        self.achievements = {"First Win": False, "Win Streak 3": False, "First Tie": False, "Loss Streak 3": False}
        self.theme = "Light"
        self.timer_seconds = 10
        self.timer_running = False
        self.game_log = []
        self.chat_log = []
        self.network_player_choice = None

        pygame.mixer.init()
        self.win_sound = pygame.mixer.Sound("win.wav")
        self.lose_sound = pygame.mixer.Sound("lose.wav")
        self.tie_sound = pygame.mixer.Sound("tie.wav")

        self.load_settings()  # Load user settings on startup

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Reset Leaderboard", command=self.reset_leaderboard)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Change Difficulty", command=self.change_difficulty)
        settings_menu.add_command(label="User Settings", command=self.user_settings)
        settings_menu.add_command(label="Change Theme", command=self.change_theme)
        settings_menu.add_command(label="Toggle Sound", command=self.toggle_sound)

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

        self.timer_label = tk.Label(self.root, text="Time Left: 10 seconds", font=("Helvetica", 14))
        self.timer_label.pack(pady=20)

        self.chat_box = scrolledtext.ScrolledText(self.root, height=10, width=50)
        self.chat_box.pack(pady=20)
        self.chat_entry = tk.Entry(self.root)
        self.chat_entry.pack(pady=10)
        self.chat_send_button = tk.Button(self.root, text="Send", command=self.send_chat)
        self.chat_send_button.pack(pady=5)

        self.game_log_button = tk.Button(self.root, text="Show Game Log", command=self.show_game_log)
        self.game_log_button.pack(pady=10)

        self.stats_button = tk.Button(self.root, text="Show Statistics", command=self.show_statistics)
        self.stats_button.pack(pady=10)

    def new_game(self):
        self.player1_name = simpledialog.askstring("Player 1 Name", "Enter name for Player 1:")
        game_mode = simpledialog.askinteger("Game Mode", "Choose game mode:\n1 for single player\n2 for two players")
        if game_mode == 2:
            self.player2_name = simpledialog.askstring("Player 2 Name", "Enter name for Player 2:")
        else:
            self.player2_name = "Computer"

        self.rounds = simpledialog.askinteger("Rounds", "Choose number of rounds (3, 5, 7):")
        self.score = {"player1": 0, "player2": 0, "ties": 0}
        self.update_score_label()
        self.start_timer()

    def play_round(self):
        if not self.player1_name:
            messagebox.showwarning("No Game", "Please start a new game from the menu.")
            return

        player1_choice = self.choice_var.get()
        player2_choice = self.get_ai_choice() if self.player2_name == "Computer" else simpledialog.askstring("Player 2 Choice", f"{self.player2_name}, choose: rock, paper, or scissors:")

        if player2_choice not in ["rock", "paper", "scissors"]:
            messagebox.showwarning("Invalid Choice", "Invalid choice for Player 2.")
            return

        self.animate_choices(player1_choice, player2_choice)
        result = self.determine_winner(player1_choice, player2_choice)
        self.check_achievements(result)
        self.update_statistics(result)

        if result == "tie":
            self.score["ties"] += 1
            self.tie_sound.play()
        elif result == "player1":
            self.score["player1"] += 1
            self.win_sound.play()
        else:
            self.score["player2"] += 1
            self.lose_sound.play()

        self.update_score_label()
        self.game_log.append(f"{self.player1_name} chose {player1_choice}, {self.player2_name} chose {player2_choice} - {result.capitalize()}")

        if self.score["player1"] > self.rounds // 2 or self.score["player2"] > self.rounds // 2:
            self.end_game()

    def get_ai_choice(self):
        if self.difficulty == "easy":
            return random.choice(["rock", "paper", "scissors"])
        elif self.difficulty == "medium":
            # Medium AI logic: slightly favoring winning move based on previous round
            last_choice = self.game_log[-1].split(" ")[-3] if self.game_log else random.choice(["rock", "paper", "scissors"])
            if last_choice == "rock":
                return random.choice(["rock", "paper"])
            elif last_choice == "paper":
                return random.choice(["paper", "scissors"])
            else:
                return random.choice(["scissors", "rock"])
        else:
            # Hard AI logic: more strategic decisions
            win_counts = {"rock": 0, "paper": 0, "scissors": 0}
            for log in self.game_log:
                choice = log.split(" ")[-3]
                if "Player 1 wins" in log:
                    win_counts[choice] += 1
            return max(win_counts, key=win_counts.get)

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

    def reset_leaderboard(self):
        self.high_scores = []
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

    def show_about(self):
        messagebox.showinfo("About", "Rock, Paper, Scissors Game\nVersion 1.0\nCreated by ChatGPT")

    def animate_choices(self, player1_choice, player2_choice):
        anim_text = f"{self.player1_name} chose {player1_choice}, {self.player2_name} chose {player2_choice}..."
        anim_label = tk.Label(self.root, text=anim_text, font=("Helvetica", 12))
        anim_label.pack(pady=10)
        self.root.update()
        time.sleep(1)
        anim_label.destroy()

    def check_achievements(self, result):
        if result == "player1" and not self.achievements["First Win"]:
            self.achievements["First Win"] = True
            messagebox.showinfo("Achievement Unlocked", "You unlocked the First Win achievement!")

        if result == "tie" and not self.achievements["First Tie"]:
            self.achievements["First Tie"] = True
            messagebox.showinfo("Achievement Unlocked", "You unlocked the First Tie achievement!")

        if self.score["player2"] >= 3 and not self.achievements["Loss Streak 3"]:
            self.achievements["Loss Streak 3"] = True
            messagebox.showinfo("Achievement Unlocked", "You unlocked the Loss Streak 3 achievement!")

        if self.score["player1"] >= 3 and not self.achievements["Win Streak 3"]:
            self.achievements["Win Streak 3"] = True
            messagebox.showinfo("Achievement Unlocked", "You unlocked the Win Streak 3 achievement!")

    def update_statistics(self, result):
        if result == "tie":
            self.player_stats["player1"]["ties"] += 1
            self.player_stats["player2"]["ties"] += 1
        elif result == "player1":
            self.player_stats["player1"]["wins"] += 1
            self.player_stats["player2"]["losses"] += 1
        else:
            self.player_stats["player1"]["losses"] += 1
            self.player_stats["player2"]["wins"] += 1

    def start_timer(self):
        self.timer_seconds = 10
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.timer_label.config(text=f"Time Left: {self.timer_seconds} seconds")
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.timer_label.config(text=f"Time's up!")
                self.play_round()

    def change_difficulty(self):
        difficulty = simpledialog.askstring("Change Difficulty", "Enter new difficulty (easy, medium, hard):")
        if difficulty in ["easy", "medium", "hard"]:
            self.difficulty = difficulty
            messagebox.showinfo("Difficulty Changed", f"Difficulty set to {difficulty}.")
        else:
            messagebox.showwarning("Invalid Difficulty", "Invalid difficulty setting.")

    def user_settings(self):
        settings = simpledialog.askstring("User Settings", "Enter your settings (theme, sound) separated by comma:")
        if settings:
            settings_list = settings.split(",")
            if len(settings_list) == 2:
                self.theme = settings_list[0].strip()
                self.sound_on = settings_list[1].strip().lower() == "on"
                self.save_settings()
                messagebox.showinfo("User Settings Updated", f"Theme set to {self.theme}, Sound {'On' if self.sound_on else 'Off'}.")
            else:
                messagebox.showwarning("Invalid Settings", "Please enter two settings (theme, sound).")

    def change_theme(self):
        themes = ["Light", "Dark"]
        theme = simpledialog.askstring("Change Theme", f"Choose new theme: {', '.join(themes)}")
        if theme in themes:
            self.theme = theme
            self.save_settings()
            messagebox.showinfo("Theme Changed", f"Theme set to {theme}.")
        else:
            messagebox.showwarning("Invalid Theme", "Invalid theme selection.")

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.save_settings()
        messagebox.showinfo("Sound Toggled", f"Sound {'On' if self.sound_on else 'Off'}.")

    def save_settings(self):
        settings = {"theme": self.theme, "sound_on": self.sound_on}
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.theme = settings.get("theme", "Light")
                self.sound_on = settings.get("sound_on", True)
        except FileNotFoundError:
            print("No settings file found. Using default settings.")

    def show_game_log(self):
        game_log_text = "\n".join(self.game_log)
        messagebox.showinfo("Game Log", game_log_text)

    def show_statistics(self):
        stats_text = "Game Statistics:\n"
        stats_text += f"{self.player1_name}: Wins - {self.player_stats['player1']['wins']}, Losses - {self.player_stats['player1']['losses']}, Ties - {self.player_stats['player1']['ties']}\n"
        stats_text += f"{self.player2_name}: Wins - {self.player_stats['player2']['wins']}, Losses - {self.player_stats['player2']['losses']}, Ties - {self.player_stats['player2']['ties']}"
        messagebox.showinfo("Game Statistics", stats_text)

    def send_chat(self):
        message = self.chat_entry.get()
        if message:
            self.chat_log.append(f"{self.player1_name}: {message}")
            self.chat_box.insert(tk.END, f"{self.player1_name}: {message}\n")
            self.chat_entry.delete(0, tk.END)

    def receive_chat(self):
        HOST = '127.0.0.1'  
        PORT = 65432        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

    def network_game(self):
        threading.Thread(target=self.receive_chat).start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 65432))
        with s:
            s.sendall(b'rock')
            data = s.recv(1024)
        print('Received', repr(data))

    def show_about(self):
        messagebox.showinfo("About", "Rock, Paper, Scissors Game\nVersion 1.0\nCreated by ChatGPT")


if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
