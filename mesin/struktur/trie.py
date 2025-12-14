class TrieNode:
    def __init__(self, char=None):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0
        self.char = char

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        
        node.is_end_of_word = True
        node.frequency += 1

    def _find_node(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def suggest(self, prefix: str):
        node = self._find_node(prefix)
        if not node:
            return []

        suggestions = []
        self._collect_all_words(node, prefix, suggestions)
        
        for i in range(1, len(suggestions)):
            key_item = suggestions[i]
            key_freq = key_item[1]
            
            j = i = 1
            while j >= 0 and suggestions[j][1] < key_freq:
                suggestions[j + 1] = suggestions[j]
                j -= 1
            
            suggestions[j + 1] = key_item
        return suggestions

        # Urutkan saran berdasarkan frekuensi secara descending
        # return sorted(suggestions, key=lambda x: x[1], reverse=True)

    def _collect_all_words(self, node: TrieNode, prefix: str, suggestions: list):

        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))

        for char, child_node in node.children.items():
            self._collect_all_words(child_node, prefix + char, suggestions)
