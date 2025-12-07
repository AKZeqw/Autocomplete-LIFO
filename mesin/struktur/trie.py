class TrieNode:
    """
    Kelas untuk satu node dalam Trie.
    
    Attributes:
        children (dict): Dictionary yang memetakan karakter ke TrieNode anak.
        is_end_of_word (bool): True jika node ini menandai akhir sebuah kata.
        frequency (int): Menyimpan frekuensi kata jika is_end_of_word True.
        char (str): Karakter yang disimpan di node ini (opsional, untuk debugging/visualisasi).
    """
    def __init__(self, char=None):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0
        self.char = char

class Trie:
    """
    Kelas implementasi struktur data Trie.
    
    Methods:
        insert(word): Memasukkan sebuah kata ke dalam Trie.
        _find_node(prefix): Mencari node terakhir dari sebuah prefix.
        suggest(prefix): Memberikan daftar saran kata berdasarkan prefix.
        _collect_all_words(node, prefix, suggestions): Helper rekursif untuk mengumpulkan kata.
    """
    def __init__(self):
        """
        Inisialisasi Trie dengan sebuah root node kosong.
        """
        self.root = TrieNode()

    def insert(self, word: str):
        """
        Memasukkan sebuah kata ke dalam Trie.
        Jika kata sudah ada, tingkatkan frekuensinya.
        
        :param word: Kata yang akan dimasukkan (string).
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        
        node.is_end_of_word = True
        node.frequency += 1

    def _find_node(self, prefix: str):
        """
        Mencari node yang merepresentasikan akhir dari sebuah prefix.
        
        :param prefix: Prefix yang akan dicari.
        :return: TrieNode jika prefix ditemukan, None jika tidak.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def suggest(self, prefix: str):
        """
        Menghasilkan daftar kata-kata saran untuk sebuah prefix.
        Saran diurutkan berdasarkan frekuensi (tertinggi ke terendah).
        
        :param prefix: Prefix untuk menghasilkan saran.
        :return: List dari tuple (kata, frekuensi) yang disarankan.
        """
        node = self._find_node(prefix)
        if not node:
            return []

        suggestions = []
        self._collect_all_words(node, prefix, suggestions)
        
        # Urutkan saran berdasarkan frekuensi secara descending
        return sorted(suggestions, key=lambda x: x[1], reverse=True)

    def _collect_all_words(self, node: TrieNode, prefix: str, suggestions: list):
        """
        Fungsi helper rekursif untuk mengumpulkan semua kata dari node tertentu.
        
        :param node: Node awal untuk mulai mengumpulkan.
        :param prefix: Prefix saat ini yang membentuk kata.
        :param suggestions: List untuk menyimpan hasil (kata, frekuensi).
        """
        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))

        for char, child_node in node.children.items():
            self._collect_all_words(child_node, prefix + char, suggestions)
