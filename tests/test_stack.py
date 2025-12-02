import unittest
import sys
import os

# Path setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mesin.struktur.stack import Stack

class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)
        self.assertIsNone(s.pop())

    def test_peek(self):
        s = Stack()
        s.push("A")
        self.assertEqual(s.peek(), "A")
        self.assertEqual(s.size(), 1) # Peek tidak menghapus

if __name__ == '__main__':
    unittest.main()