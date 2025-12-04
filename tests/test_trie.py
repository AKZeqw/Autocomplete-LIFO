"""
File: test_trie.py

Unit test untuk kelas Trie.
"""
import unittest
import sys
import os

# Menambahkan parent directory ke path agar bisa import modul dari `mesin`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mesin.struktur.trie import Trie

class TestTrie(unittest.TestCase):
    """
    Test suite untuk kelas Trie.
    """

    def setUp(self):
        """
        Metode ini dijalankan sebelum setiap metode test.
        Inisialisasi trie baru untuk setiap test case.
        """
        self.trie = Trie()

    def test_insert_single_word(self):
        """
        Test memasukkan satu kata.
        """
        self.trie.insert("halo")
        node = self.trie._find_node("halo")
        self.assertIsNotNone(node)
        self.assertTrue(node.is_end_of_word)
        self.assertEqual(node.frequency, 1)

    def test_insert_multiple_words(self):
        """
        Test memasukkan beberapa kata dengan prefix yang sama.
        """
        words = ["kucing", "kuda", "kumbang"]
        for word in words:
            self.trie.insert(word)

        # Cek prefix "ku"
        node_ku = self.trie._find_node("ku")
        self.assertIsNotNone(node_ku)
        self.assertFalse(node_ku.is_end_of_word) # "ku" bukan kata

        # Cek kata "kucing"
        node_kucing = self.trie._find_node("kucing")
        self.assertTrue(node_kucing.is_end_of_word)
        self.assertEqual(node_kucing.frequency, 1)
        
        # Cek kata "kuda"
        node_kuda = self.trie._find_node("kuda")
        self.assertTrue(node_kuda.is_end_of_word)
        self.assertEqual(node_kuda.frequency, 1)

    def test_insert_frequency(self):
        """
        Test frekuensi kata akan bertambah jika di-insert berulang kali.
        """
        self.trie.insert("tes")
        self.trie.insert("tes")
        self.trie.insert("tes")
        node = self.trie._find_node("tes")
        self.assertEqual(node.frequency, 3)

    def test_find_node_not_exist(self):
        """
        Test mencari prefix yang tidak ada dalam trie.
        """
        self.trie.insert("ada")
        node = self.trie._find_node("tidakada")
        self.assertIsNone(node)

    def test_suggest_simple(self):
        """
        Test fungsi suggest dengan kasus sederhana.
        """
        words = ["mobil", "motor", "mouse"]
        for word in words:
            self.trie.insert(word)
        
        suggestions = self.trie.suggest("mo")
        suggestion_words = [s[0] for s in suggestions]
        
        self.assertIn("mobil", suggestion_words)
        self.assertIn("motor", suggestion_words)
        self.assertIn("mouse", suggestion_words)
        self.assertEqual(len(suggestion_words), 3)

    def test_suggest_no_match(self):
        """
        Test suggest untuk prefix yang tidak memiliki kecocokan.
        """
        self.trie.insert("kata")
        suggestions = self.trie.suggest("xyz")
        self.assertEqual(suggestions, [])

    def test_suggest_is_a_word(self):
        """
        Test suggest di mana prefix itu sendiri adalah sebuah kata.
        """
        words = ["data", "database", "datang"]
        self.trie.insert("data")
        self.trie.insert("database")
        self.trie.insert("datang")
        
        suggestions = self.trie.suggest("data")
        suggestion_words = [s[0] for s in suggestions]
        
        self.assertIn("data", suggestion_words)
        self.assertIn("database", suggestion_words)
        self.assertIn("datang", suggestion_words)

    def test_suggest_ordering_by_frequency(self):
        """
        Test bahwa hasil suggest diurutkan berdasarkan frekuensi.
        """
        self.trie.insert("saran") # freq 1
        self.trie.insert("sarat")
        self.trie.insert("sarat")
        self.trie.insert("sarat") # freq 3
        self.trie.insert("sarang")
        self.trie.insert("sarang") # freq 2

        suggestions = self.trie.suggest("sara")
        
        # Hasil harus: ('sarat', 3), ('sarang', 2), ('saran', 1)
        self.assertEqual(len(suggestions), 3)
        self.assertEqual(suggestions[0], ("sarat", 3))
        self.assertEqual(suggestions[1], ("sarang", 2))
        self.assertEqual(suggestions[2], ("saran", 1))

if __name__ == '__main__':
    unittest.main()
