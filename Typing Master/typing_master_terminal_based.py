import random
import time
import json
from colorama import Fore, Style, init

init(autoreset=True)

# Constants
WORD_LIST_FILE = 'word_categories.json'
LEADERBOARD_FILE = 'leaderboard.json'
CORRECT = Fore.GREEN + 'Correct!' + Style.RESET_ALL
INCORRECT = Fore.RED + 'Incorrect!' + Style.RESET_ALL

# Function to load words from a JSON file
def load_words_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to update the leaderboard
def update_leaderboard(username, wpm, category):
    leaderboard = load_words_from_json(LEADERBOARD_FILE)
    leaderboard_entry = {"username": username, "wpm": wpm, "category": category}
    
    if "leaderboard" not in leaderboard:
        leaderboard["leaderboard"] = []

    leaderboard["leaderboard"].append(leaderboard_entry)
    leaderboard["leaderboard"].sort(key=lambda x: x["wpm"], reverse=True)
    
    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(leaderboard, file, indent=2)

# Function to display the leaderboard
def show_leaderboard():
    leaderboard = load_words_from_json(LEADERBOARD_FILE).get("leaderboard", [])
    print("--- Leaderboard ---")
    for idx, entry in enumerate(leaderboard, start=1):
        print(f"{idx}. {entry['username']} - {entry['wpm']} WPM (Category: {entry['category']})")

# Function to run the typing test
def run_typing_test(username, category, num_words):
    words = load_words_from_json(WORD_LIST_FILE)[category]
    random.shuffle(words)
    selected_words = words[:num_words]
    start_time = time.time()
    correct_words = 0

    print(f"Welcome, {username}! Press 'Ctrl + Q' to quit at any time.")
    input("Press any key to start...")

    for word in selected_words:
        user_input = input(f"Type: {word} ")
        if user_input == word:
            print(CORRECT)
            correct_words += 1
        elif user_input == "Ctrl + Q":
            break
        else:
            print(INCORRECT)

    end_time = time.time()
    elapsed_time = end_time - start_time
    wpm = (correct_words / elapsed_time) * 60

    print(f"Typing Metrics for {username}:")
    print(f"Words Typed: {correct_words}")
    print(f"Time Taken: {elapsed_time:.2f} seconds")
    print(f"Words Per Minute: {wpm:.2f}")

    update_leaderboard(username, wpm, category)

# Main function
def main():
    print("Welcome to Terminal Typing Master!")

    # Get user information
    username = input("Enter your username: ")

    while True:
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Choose a category:")
            categories = load_words_from_json(WORD_LIST_FILE).keys()
            for idx, category in enumerate(categories, start=1):
                print(f"{idx}. {category}")
            
            category_choice = input("Enter the number for your chosen category: ")
            category_choice = int(category_choice) - 1
            if category_choice < 0 or category_choice >= len(categories):
                print("Invalid category choice.")
                continue

            num_words = int(input("Enter the number of words to practice (1-200): "))
            if num_words < 1 or num_words > 200:
                print("Invalid number of words.")
                continue

            run_typing_test(username, list(categories)[category_choice], num_words)

        elif choice == '2':
            show_leaderboard()

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
