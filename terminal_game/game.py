import random
import time
import os

leaderboard_file = "leaderboard.txt"

def set_difficulty():
    while True:
        difficulty = input("Choose difficulty level (easy, medium, hard): ").lower()
        if difficulty == "easy":
            return 1, 50, 10
        elif difficulty == "medium":
            return 1, 100, 7
        elif difficulty == "hard":
            return 1, 200, 5
        else:
            print("Invalid choice. Please select easy, medium, or hard.")

def play_game():
    low, high, max_attempts = set_difficulty()
    number_to_guess = random.randint(low, high)
    attempts = 0
    score = 100
    hints_used = 0

    print(f"Welcome to 'Guess the Number'! I've selected a number between {low} and {high}. Can you guess what it is?")
    
    start_time = time.time()

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            score -= 10

            if guess < number_to_guess:
                print("Too low! Try again.")
                os.system('play -nq -t alsa synth 0.1 sine 440')  # Optional: Sound for incorrect guess
            elif guess > number_to_guess:
                print("Too high! Try again.")
                os.system('play -nq -t alsa synth 0.1 sine 440')  # Optional: Sound for incorrect guess
            else:
                elapsed_time = time.time() - start_time
                print(f"Congratulations! You've guessed the number in {attempts} attempts with a score of {score} and time of {elapsed_time:.2f} seconds.")
                os.system('play -nq -t alsa synth 0.1 sine 880')  # Optional: Sound for correct guess
                update_leaderboard(score, elapsed_time)
                break

            if attempts == max_attempts // 2:
                hint = "even" if number_to_guess % 2 == 0 else "odd"
                print(f"Hint: The number is {hint}.")
                hints_used += 1

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    if attempts >= max_attempts:
        print(f"Sorry, you've used all your attempts. The number was {number_to_guess}. Your score is {score}.")
    
    print(f"Game over! Total hints used: {hints_used}")

def update_leaderboard(score, elapsed_time):
    name = input("Enter your name for the leaderboard: ")
    with open(leaderboard_file, "a") as file:
        file.write(f"{name} {score} {elapsed_time:.2f}\n")
    print("Leaderboard updated!")

def display_leaderboard():
    if os.path.exists(leaderboard_file):
        print("\n--- Leaderboard ---")
        with open(leaderboard_file, "r") as file:
            scores = [line.strip().split() for line in file.readlines()]
            scores = sorted(scores, key=lambda x: (-int(x[1]), float(x[2])))[:10]
            for i, entry in enumerate(scores, 1):
                print(f"{i}. {entry[0]} - Score: {entry[1]}, Time: {entry[2]}s")
    else:
        print("No scores yet. Be the first to play and get on the leaderboard!")

def main():
    while True:
        play_game()
        display_leaderboard()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()
