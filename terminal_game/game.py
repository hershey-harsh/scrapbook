import random
import time
import os
import json
from datetime import datetime

# File paths for storing profiles, leaderboard, and daily challenge
profile_file = "profiles.json"
leaderboard_file = "leaderboard.txt"
daily_challenge_file = "daily_challenge.json"

# Load profiles from file
def load_profiles():
    if os.path.exists(profile_file):
        with open(profile_file, "r") as file:
            return json.load(file)
    return {}

# Save profiles to file
def save_profiles(profiles):
    with open(profile_file, "w") as file:
        json.dump(profiles, file)

# Load daily challenge from file
def load_daily_challenge():
    if os.path.exists(daily_challenge_file):
        with open(daily_challenge_file, "r") as file:
            return json.load(file)
    else:
        daily_challenge = {"date": "", "number": 0}
        save_daily_challenge(daily_challenge)
        return daily_challenge

# Save daily challenge to file
def save_daily_challenge(daily_challenge):
    with open(daily_challenge_file, "w") as file:
        json.dump(daily_challenge, file)

# Set difficulty levels
def set_difficulty(level):
    if level == 1:
        return 1, 50, 10
    elif level == 2:
        return 1, 100, 7
    elif level == 3:
        return 1, 200, 5
    else:
        return 1, 300, 3

# Generate daily challenge number
def generate_daily_challenge():
    daily_challenge = load_daily_challenge()
    today = datetime.today().strftime('%Y-%m-%d')
    if daily_challenge["date"] != today:
        daily_challenge["date"] = today
        daily_challenge["number"] = random.randint(1, 100)
        save_daily_challenge(daily_challenge)
    return daily_challenge["number"]

# Function to play the game
def play_game(profile, game_mode):
    if game_mode == "daily":
        number_to_guess = generate_daily_challenge()
        low, high, max_attempts = 1, 100, 10
        print("Welcome to the Daily Challenge! I've selected a number between 1 and 100. Can you guess what it is?")
    elif game_mode == "endless":
        low, high, max_attempts = set_difficulty(profile.get("level", 1))
        number_to_guess = random.randint(low, high)
        print("Welcome to Endless Mode! Try to guess the number as many times as you can.")
    elif game_mode == "versus":
        print("Welcome to Versus Mode! Two players will take turns guessing the number.")
        versus_mode(profile)
        return
    else:
        level = profile.get("level", 1)
        hints = profile.get("hints", 1)
        low, high, max_attempts = set_difficulty(level)
        number_to_guess = random.randint(low, high)
        print(f"Welcome to 'Guess the Number' Level {level}! I've selected a number between {low} and {high}. Can you guess what it is?")
    
    attempts = 0
    score = 100
    hints_used = 0
    start_time = time.time()

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            score -= 10

            if guess < number_to_guess:
                print("Too low! Try again.")
                if profile["settings"]["sound"]:
                    os.system('play -nq -t alsa synth 0.1 sine 440')
            elif guess > number_to_guess:
                print("Too high! Try again.")
                if profile["settings"]["sound"]:
                    os.system('play -nq -t alsa synth 0.1 sine 440')
            else:
                elapsed_time = time.time() - start_time
                print(f"Congratulations! You've guessed the number in {attempts} attempts with a score of {score} and time of {elapsed_time:.2f} seconds.")
                if profile["settings"]["sound"]:
                    os.system('play -nq -t alsa synth 0.1 sine 880')
                if game_mode != "daily":
                    update_leaderboard(profile['name'], score, elapsed_time, profile['level'], game_mode)
                    profile["level"] += 1
                    profile["hints"] += 1 if hints_used == 0 else 0
                    profile["stats"]["games_played"] += 1
                    profile["stats"]["total_score"] += score
                    profile["stats"]["average_score"] = profile["stats"]["total_score"] / profile["stats"]["games_played"]
                    check_achievements(profile, attempts, elapsed_time)
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

# Versus mode functionality
def versus_mode(profile):
    player1_name = profile["name"]
    player2_name = input("Enter the name of Player 2: ")
    player1_score = 0
    player2_score = 0
    rounds = 3

    for i in range(rounds):
        print(f"\nRound {i+1} - {player1_name}'s turn")
        number_to_guess = random.randint(1, 100)
        attempts = 0
        while attempts < 10:
            try:
                guess = int(input(f"{player1_name}, enter your guess: "))
                attempts += 1
                if guess < number_to_guess:
                    print("Too low! Try again.")
                elif guess > number_to_guess:
                    print("Too high! Try again.")
                else:
                    print(f"Congratulations {player1_name}! You've guessed the number in {attempts} attempts.")
                    player1_score += 10 - attempts
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        print(f"\nRound {i+1} - {player2_name}'s turn")
        number_to_guess = random.randint(1, 100)
        attempts = 0
        while attempts < 10:
            try:
                guess = int(input(f"{player2_name}, enter your guess: "))
                attempts += 1
                if guess < number_to_guess:
                    print("Too low! Try again.")
                elif guess > number_to_guess:
                    print("Too high! Try again.")
                else:
                    print(f"Congratulations {player2_name}! You've guessed the number in {attempts} attempts.")
                    player2_score += 10 - attempts
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    
    print("\n--- Versus Mode Results ---")
    print(f"{player1_name} Score: {player1_score}")
    print(f"{player2_name} Score: {player2_score}")
    if player1_score > player2_score:
        print(f"{player1_name} wins!")
    elif player2_score > player1_score:
        print(f"{player2_name} wins!")
    else:
        print("It's a tie!")

# Update leaderboard with new scores
def update_leaderboard(name, score, elapsed_time, level, game_mode):
    with open(leaderboard_file, "a") as file:
        file.write(f"{name} {score} {elapsed_time:.2f} {level} {game_mode}\n")
    print("Leaderboard updated!")

# Display the leaderboard
def display_leaderboard():
    if os.path.exists(leaderboard_file):
        print("\n--- Leaderboard ---")
        with open(leaderboard_file, "r") as file:
            scores = [line.strip().split() for line in file.readlines()]
            scores = sorted(scores, key=lambda x: (-int(x[1]), float(x[2]), -int(x[3])))[:10]
            for i, entry in enumerate(scores, 1):
                print(f"{i}. {entry[0]} - Score: {entry[1]}, Time: {entry[2]}s, Level: {entry[3]}, Mode: {entry[4]}")
    else:
        print("No scores yet. Be the first to play and get on the leaderboard!")

# Check and unlock achievements
def check_achievements(profile, attempts, elapsed_time):
    achievements = profile.get("achievements", [])
    if attempts == 1:
        achievements.append("First Try!")
        print("Achievement unlocked: First Try!")
    if elapsed_time < 10:
        achievements.append("Quick Guess!")
        print("Achievement unlocked: Quick Guess!")
    if profile["level"] == 10:
        achievements.append("Level 10!")
        print("Achievement unlocked: Level 10!")
    if profile["stats"]["total_score"] >= 1000:
        achievements.append("Score 1000!")
        print("Achievement unlocked: Score 1000!")
    profile["achievements"] = list(set(achievements))

# Display player statistics
def display_stats(profile):
    stats = profile["stats"]
    print("\n--- Player Statistics ---")
    print(f"Total Games Played: {stats['games_played']}")
    print(f"Total Score: {stats['total_score']}")
    print(f"Average Score: {stats['average_score']:.2f}")

# Display achievements
def display_achievements(profile):
    achievements = profile.get("achievements", [])
    if achievements:
        print("\n--- Achievements ---")
        for achievement in achievements:
            print(f"- {achievement}")
    else:
        print("No achievements yet. Keep playing to unlock them!")

# Change settings
def change_settings(profile):
    print("\n--- Settings ---")
    print("1. Toggle Sound")
    print("2. Change Theme")
    print("3. Reset Progress")
    choice = input("Choose an option: ")
    if choice == '1':
        profile["settings"]["sound"] = not profile["settings"]["sound"]
        print(f"Sound effects {'enabled' if profile['settings']['sound'] else 'disabled'}.")
    elif choice == '2':
        profile["settings"]["theme"] = input("Enter theme (default, dark, light): ")
        print(f"Theme changed to {profile['settings']['theme']}.")
    elif choice == '3':
        profile["level"] = 1
        profile["hints"] = 1
        profile["achievements"] = []
        profile["stats"] = {"games_played": 0, "total_score": 0, "average_score": 0}
        print("Progress reset.")
    else:
        print("Invalid choice. Please select a valid option.")

# Main function to run the game
def main():
    profiles = load_profiles()
    name = input("Enter your name: ")
    if name in profiles:
        profile = profiles[name]
        print(f"Welcome back, {name}! Resuming from level {profile['level']} with {profile['hints']} hints.")
    else:
        profile = {"name": name, "level": 1, "hints": 1, "achievements": [], "stats": {"games_played": 0, "total_score": 0, "average_score": 0}, "settings": {"sound": True, "theme": "default"}}
        profiles[name] = profile

    while True:
        print("\n1. Play Normal Mode\n2. Play Timed Mode\n3. Play Limited Guess Mode\n4. Play Daily Challenge\n5. Play Endless Mode\n6. Play Versus Mode\n7. Display Statistics\n8. Display Achievements\n9. Settings\n10. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            play_game(profile, "normal")
        elif choice == '2':
            play_game(profile, "timed")
        elif choice == '3':
            play_game(profile, "limited")
        elif choice == '4':
            play_game(profile, "daily")
        elif choice == '5':
            play_game(profile, "endless")
        elif choice == '6':
            play_game(profile, "versus")
        elif choice == '7':
            display_stats(profile)
        elif choice == '8':
            display_achievements(profile)
        elif choice == '9':
            change_settings(profile)
        elif choice == '10':
            save_profiles(profiles)
            print("Thanks for playing! Your progress has been saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
        display_leaderboard()

if __name__ == "__main__":
    main()
