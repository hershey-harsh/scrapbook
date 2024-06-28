import random
import time

def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    score = {"player1": 0, "player2": 0, "ties": 0}

    def countdown_timer():
        print("Get ready to choose in:")
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)

    print("Welcome to Rock, Paper, Scissors!")
    game_mode = input("Choose game mode: 1 for single player, 2 for two players: ")

    if game_mode == "1":
        print("Type 'exit' to end the game.")
        rounds = int(input("Choose number of rounds (best of 3, 5, 7): "))

        while True:
            computer_choice = random.choice(choices)
            
            countdown_timer()
            player_choice = input("Please choose: rock, paper, or scissors: ").lower()

            if player_choice == "exit":
                print("Thanks for playing!")
                print(f"Final score - Wins: {score['player1']}, Losses: {score['player2']}, Ties: {score['ties']}")
                break

            if player_choice not in choices:
                print("Invalid choice! Please choose rock, paper, or scissors.")
                continue

            print(f"Computer chose: {computer_choice}")
            print(f"You chose: {player_choice}")

            if player_choice == computer_choice:
                print("It's a tie!")
                score["ties"] += 1
            elif (player_choice == "rock" and computer_choice == "scissors") or \
                (player_choice == "scissors" and computer_choice == "paper") or \
                (player_choice == "paper" and computer_choice == "rock"):
                print("You win!")
                score["player1"] += 1
            else:
                print("You lose!")
                score["player2"] += 1

            print(f"Current score - Wins: {score['player1']}, Losses: {score['player2']}, Ties: {score['ties']}")

            if score["player1"] > rounds // 2 or score["player2"] > rounds // 2:
                print("Game over!")
                print(f"Final score - Wins: {score['player1']}, Losses: {score['player2']}, Ties: {score['ties']}")
                break

    elif game_mode == "2":
        rounds = int(input("Choose number of rounds (best of 3, 5, 7): "))
        while True:
            countdown_timer()
            player1_choice = input("Player 1, please choose: rock, paper, or scissors: ").lower()
            player2_choice = input("Player 2, please choose: rock, paper, or scissors: ").lower()

            if player1_choice not in choices or player2_choice not in choices:
                print("Invalid choice! Please choose rock, paper, or scissors.")
                continue

            print(f"Player 1 chose: {player1_choice}")
            print(f"Player 2 chose: {player2_choice}")

            if player1_choice == player2_choice:
                print("It's a tie!")
                score["ties"] += 1
            elif (player1_choice == "rock" and player2_choice == "scissors") or \
                (player1_choice == "scissors" and player2_choice == "paper") or \
                (player1_choice == "paper" and player2_choice == "rock"):
                print("Player 1 wins this round!")
                score["player1"] += 1
            else:
                print("Player 2 wins this round!")
                score["player2"] += 1

            print(f"Current score - Player 1: {score['player1']}, Player 2: {score['player2']}, Ties: {score['ties']}")

            if score["player1"] > rounds // 2 or score["player2"] > rounds // 2:
                print("Game over!")
                print(f"Final score - Player 1: {score['player1']}, Player 2: {score['player2']}, Ties: {score['ties']}")
                break

    else:
        print("Invalid game mode! Please restart the game and choose either 1 or 2.")

if __name__ == "__main__":
    rock_paper_scissors()
