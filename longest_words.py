from itertools import permutations

# Load the word dictionary
def load_words(file_path):
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file)

# Find all permutations of the given letters
def find_permutations(letters):
    return set(''.join(p) for i in range(1, len(letters) + 1) for p in permutations(letters, i))

# Find the longest valid words from the permutations
def find_longest_words(letters, word_dict):
    perms = find_permutations(letters)
    valid_words = [word for word in perms if word in word_dict]
    max_length = max(len(word) for word in valid_words) if valid_words else 0
    longest_words = [word for word in valid_words if len(word) == max_length]
    return longest_words

# Main function
def main():
    letters = input("Enter 9 scrambled letters: ").lower()
    #if len(letters) != 9:
    #    print("Please enter exactly 9 letters.")
    #    return
    
    word_dict = load_words('words_alpha.txt')
    longest_words = find_longest_words(letters, word_dict)
    
    if longest_words:
        print(f"The longest words you can make are: {', '.join(longest_words)}")
    else:
        print("No valid words found.")

if __name__ == "__main__":
    main()
