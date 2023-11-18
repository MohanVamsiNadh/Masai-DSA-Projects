import difflib

class CustomTrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class CustomTrie:
    def __init__(self):
        self.root = CustomTrieNode()

    def insert_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = CustomTrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def get_all_words(self, node=None, current_prefix='', all_words=None):
        if node is None:
            node = self.root
        if all_words is None:
            all_words = []
        if node.is_end_of_word:
            all_words.append(current_prefix)
        for char, child_node in node.children.items():
            self.get_all_words(child_node, current_prefix + char, all_words)
        return all_words

def suggest_corrections(input_word, custom_trie, threshold=0.15):
    suggestions = []
    trie_words = custom_trie.get_all_words()
    close_matches = difflib.get_close_matches(input_word, trie_words, n=5, cutoff=threshold)

    for match in close_matches:
        suggestions.append(match)

    return set(suggestions)

def main():
    custom_trie = CustomTrie()

    with open("popular.txt", "r") as file:
        trie_words = [line.strip() for line in file]

    for word in trie_words:
        custom_trie.insert_word(word)

    user_input = input("my_word = ")
    if user_input.isalpha():
        if custom_trie.search_word(user_input):
            print(f"'{user_input}' is a valid word.")
        else:
            suggested_corrections = suggest_corrections(user_input, custom_trie)
            if suggested_corrections:
                print(f"Did you mean: {suggested_corrections} ?")
            else:
                print(f"No suggestions found for '{user_input}'.")
    else:
        print("Only alphabetic input is accepted.")

if __name__ == "__main__":
    main()
