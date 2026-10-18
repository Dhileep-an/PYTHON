# project2.py
# Number Guessing Game & Word Counter

import random
import string
from collections import Counter

def play_game(best_score):
    '''Runs the Number Guessing Game and returns the updated best score.'''
    while True:
        print("\n--- Number Guessing Game ---")
        secret_number = random.randint(1, 100)
        attempts = 0
        max_attempts = 10
        score = 100
        
        print("I'm thinking of a number between 1 and 100.")
        print(f"You have {max_attempts} attempts. Starting score: {score}")
        
        won = False
        while attempts < max_attempts:
            guess_str = input(f"Attempt {attempts + 1}/{max_attempts} - Enter your guess: ").strip()
            
            try:
                guess = int(guess_str)
            except ValueError:
                print("Invalid input. Please enter a whole number.")
                continue
                
            attempts += 1
            
            if guess < secret_number:
                print("Too low!")
                score -= 10
            elif guess > secret_number:
                print("Too high!")
                score -= 10
            else:
                print(f"Correct! You guessed the number in {attempts} attempts.")
                won = True
                break
                
        if not won:
            print(f"Game over! You've run out of attempts. The number was {secret_number}.")
            score = 0
            
        print(f"Your score for this round: {score}")
        
        if best_score is None or score > best_score:
            print("New Best Score!")
            best_score = score
            
        print(f"Current Best Score: {best_score}")
        
        play_again = input("Do you want to play again? (y/n): ").strip().lower()
        if play_again != 'y':
            break
            
    return best_score

def count_words(path="sample.txt"):
    '''Reads a text file, cleans punctuation/case, and prints word frequencies.'''
    print(f"\n--- Word Counter ({path}) ---")
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"File not found: {path}. Please ensure the file exists in the directory.")
        return

    # Remove punctuation using str.translate
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    counts = Counter(words)
    
    if counts:
        print(f"Total words: {sum(counts.values())}")
        print(f"Unique words: {len(counts)}\n")
        print("Top 10 most common words:")
        print("-" * 25)
        for word, n in counts.most_common(10):
            print(f"{word:<15} {n:>5}")
    else:
        print("The file is empty.")

def main():
    '''Main menu loop.'''
    best_score = None
    
    while True:
        print("\n=== Main Menu ===")
        print("1) Play the game")
        print("2) Count words in a file")
        print("3) Quit")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            best_score = play_game(best_score)
        elif choice == '2':
            # Optionally let the user specify a file or default to sample.txt
            filename = input("Enter filename (press Enter for default 'sample.txt'): ").strip()
            if not filename:
                filename = "sample.txt"
            count_words(filename)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
