import re
from datetime import datetime

def load_word_list():
    """Load and filter 5-letter words from words_alpha.txt"""
    with open('words_alpha.txt', 'r') as file:
        # Convert to lowercase and filter for 5-letter words
        words = [word.strip().lower() for word in file if len(word.strip()) == 5]
    return words

def get_result_pattern(guess, result):
    """
    Convert Wordle result into a pattern for filtering
    result should be a string of 5 characters: g (green), y (yellow), or x (gray)
    """
    pattern = []
    yellow_letters = set()  # Track yellow letters to ensure they appear somewhere
    
    for i, (letter, res) in enumerate(zip(guess, result)):
        if res == 'g':  # Green - correct letter, correct position
            pattern.append(letter)
        elif res == 'y':  # Yellow - correct letter, wrong position
            pattern.append(f'[^{letter}]')  # Can't be in this position
            yellow_letters.add(letter)  # Must appear somewhere else
        else:  # Gray - letter not in word
            pattern.append(f'[^{letter}]')
    
    return ''.join(pattern), yellow_letters

def filter_words(words, guess, result, previous_constraints=None):
    """Filter words based on the guess and result, taking into account previous constraints"""
    if previous_constraints is None:
        previous_constraints = {
            'pattern': '.....',  # Any 5 letters
            'yellow_letters': set(),
            'gray_letters': set(),
            'yellow_positions': {}  # letter -> set of positions it can't be in
        }
    
    # Get current constraints
    pattern, yellow_letters = get_result_pattern(guess, result)
    
    # Update yellow positions
    yellow_positions = previous_constraints['yellow_positions'].copy()
    for pos, (letter, res) in enumerate(zip(guess, result)):
        if res == 'y':
            if letter not in yellow_positions:
                yellow_positions[letter] = set()
            yellow_positions[letter].add(pos)
    
    # Update gray letters
    gray_letters = previous_constraints['gray_letters'].copy()
    gray_letters.update(letter for letter, res in zip(guess, result) if res == 'x')
    
    # Update yellow letters
    yellow_letters.update(previous_constraints['yellow_letters'])
    
    # Filter words based on all constraints
    filtered = words
    
    # Apply pattern matching
    regex = re.compile(pattern)
    filtered = [word for word in filtered if regex.match(word)]
    
    # Apply yellow letter constraints
    for letter in yellow_letters:
        filtered = [word for word in filtered if letter in word]
        # Apply position constraints for yellow letters
        if letter in yellow_positions:
            filtered = [word for word in filtered if all(word[pos] != letter for pos in yellow_positions[letter])]
    
    # Apply gray letter constraints
    for letter in gray_letters:
        filtered = [word for word in filtered if letter not in word]
    
    return filtered, {
        'pattern': pattern,
        'yellow_letters': yellow_letters,
        'gray_letters': gray_letters,
        'yellow_positions': yellow_positions
    }

def save_solved_word(word):
    """Save a solved word to a file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('solved_words.txt', 'a') as f:
        f.write(f"{timestamp}: {word}\n")

def show_solved_words():
    """Show the history of solved words"""
    try:
        with open('solved_words.txt', 'r') as f:
            words = f.readlines()
            if words:
                print("\nPreviously solved words:")
                for word in words:
                    print(word.strip())
            else:
                print("\nNo words solved yet!")
    except FileNotFoundError:
        print("\nNo words solved yet!")

def main():
    print("Welcome to Wordle Helper!")
    print("Enter your guess and result after each guess.")
    print("Use: g for green (correct letter, correct position)")
    print("     y for yellow (correct letter, wrong position)")
    print("     x for gray (letter not in word)")
    print("Example: if you guessed 'STARE' and got: green S, yellow T, gray A, gray R, gray E")
    print("Enter: STARE")
    print("Enter result: gxxxx")
    
    words = load_word_list()
    print(f"\nLoaded {len(words)} 5-letter words")
    
    constraints = None
    while True:
        guess = input("\nEnter your guess (or 'q' to quit, 'h' to show history): ").lower()
        if guess == 'q':
            break
        elif guess == 'h':
            show_solved_words()
            continue
            
        if len(guess) != 5:
            print("Please enter a 5-letter word!")
            continue
            
        result = input("Enter result (g/y/x): ").lower()
        if len(result) != 5 or not all(c in 'gyx' for c in result):
            print("Please enter a valid result (5 characters of g/y/x)")
            continue
            
        possible_words, constraints = filter_words(words, guess, result, constraints)
        
        # Check if word is solved
        if result == 'ggggg':
            print(f"\nCongratulations! You solved the word: {guess.upper()}")
            save_solved_word(guess.upper())
        
        print(f"\nFound {len(possible_words)} possible words:")
        print(possible_words[:10])  # Show first 10 suggestions
        if len(possible_words) > 10:
            print("...")

if __name__ == "__main__":
    main() 