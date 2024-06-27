import random
import time
import os
import json

profile_file = "profiles.json"
leaderboard_file = "leaderboard.txt"

def load_profiles():
    if os.path.exists(profile_file):
        with open(profile_file, "r") as file:
            return json.load(file)
    return {}

def save_profiles(profiles):
    with open(profile_file, "w") as file:
        json.dump(profiles, file)

def set_difficulty(level):
    if level == 1:
        return 1, 50, 10
    elif level == 2:
        return 1, 100, 7
    elif level == 3:
        return 1, 200, 5
    else:
        return 1, 300, 3

def play_game(profile):
    level = profile.get("level", 1)
    hints = profile.get("hints", 1)
    low, high, max_attempts = set_difficulty(level)
    number_to_guess = random.randint(low, high)
    attempts = 0
    score = 100
    hints_used = 0

    print(f"Welcome to 'Guess the Number' Level {level}! I've selected a number between {low} and {high}. Can you guess what it is?")
    
    start_time = time.time()

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            score -= 10

            if guess < number_to_guess:
                print("Too low! Try again.")
                os.system('play -nq -t alsa synth 0.1 sine 440')
            elif guess > number_to_guess:
                print("Too high! Try again.")
                os.system('play -nq -t alsa synth 0.1 sine 440')
            else:
                elapsed_time = time.time() - start_time
                print(f"Congratulations! You've guessed the number in {attempts} attempts with a score of {score} and time of {elapsed_time:.2f} seconds.")
                os.system('play -nq -t alsa synth 0.1 sine 880')
                update_leaderboard(profile['name'], score, elapsed_time, level)
                profile["level"] += 1
                profile["hints"] += 1 if hints_used == 0 else 0
                save_profiles(profiles)
                break

            if attempts == max_attempts // 2 and hints > 0:
                hint = "even" if number_to_guess % 2 == 0 else "odd"
                print(f"Hint: The number is {hint}.")
                hints_used += 1
                profile["hints"] -= 1

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    if attempts >= max_attempts:
        print(f"Sorry, you've used all your attempts. The number was {number_to_guess}. Your score is {score}.")
    
    print(f"Game over! Total hints used: {hints_used}")

def update_leaderboard(name, score, elapsed_time, level):
    with open(leaderboard_file, "a") as file:
        file.write(f"{name} {score} {elapsed_time:.2f} {level}\n")
    print("Leaderboard updated!")

def display_leaderboard():
    if os.path.exists(leaderboard_file):
        print("\n--- Leaderboard ---")
        with open(leaderboard_file, "r") as file:
            scores = [line.strip().split() for line in file.readlines()]
            scores = sorted(scores, key=lambda x: (-int(x[1]), float(x[2]), -int(x[3])))[:10]
            for i, entry in enumerate(scores, 1):
                print(f"{i}. {entry[0]} - Score: {entry[1]}, Time: {entry[2]}s, Level: {entry[3]}")
    else:
        print("No scores yet. Be the first to play and get on the leaderboard!")

def main():
    profiles = load_profiles()
    name = input("Enter your name: ")
    if name in profiles:
        profile = profiles[name]
        print(f"Welcome back, {name}! Resuming from level {profile['level']} with {profile['hints']} hints.")
    else:
        profile = {"name": name, "level": 1, "hints": 1}
        profiles[name] = profile

    while True:
        play_game(profile)
        display_leaderboard()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Your progress has been saved. Goodbye!")
            break

if __name__ == "__main__":
    main()
