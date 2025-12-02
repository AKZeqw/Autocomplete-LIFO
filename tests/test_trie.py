import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mesin.struktur.trie import Trie

class TestTrie(unittest.TestCase):
    def test_insert_search(self):
        t = Trie()
        t.insert("algo")
        # Test autocomplete
        self.assertIn("algo", t.get_autocomplete_suggestions("al"))
        self.assertEqual(t.get_autocomplete_suggestions("x"), [])

    def test_multiple_suggestions(self):
        t = Trie()
        t.insert("teh")
        t.insert("tes")
        suggestions = t.get_autocomplete_suggestions("te")
        self.assertIn("teh", suggestions)
        self.assertIn("tes", suggestions)

if __name__ == '__main__':
    unittest.main()