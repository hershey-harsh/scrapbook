import random

def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    score = {"wins": 0, "losses": 0, "ties": 0}

    print("Welcome to Rock, Paper, Scissors!")
    print("Type 'exit' to end the game.")

    while True:
        computer_choice = random.choice(choices)
        
        player_choice = input("Please choose: rock, paper, or scissors: ").lower()
        
        if player_choice == "exit":
            print("Thanks for playing!")
            print(f"Final score - Wins: {score['wins']}, Losses: {score['losses']}, Ties: {score['ties']}")
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
            score["wins"] += 1
        else:
            print("You lose!")
            score["losses"] += 1

        print(f"Current score - Wins: {score['wins']}, Losses: {score['losses']}, Ties: {score['ties']}")

if __name__ == "__main__":
    rock_paper_scissors()
