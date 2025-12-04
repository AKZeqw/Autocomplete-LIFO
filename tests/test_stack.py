"""
File: test_stack.py

Unit test untuk kelas Stack.
"""
import unittest
import sys
import os

# Menambahkan parent directory ke path agar bisa import modul dari `mesin`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mesin.struktur.stack import Stack

class TestStack(unittest.TestCase):
    """
    Test suite untuk kelas Stack.
    """

    def setUp(self):
        """
        Metode ini dijalankan sebelum setiap metode test.
        Inisialisasi stack baru untuk setiap test case.
        """
        self.stack = Stack()

    def test_init(self):
        """
        Test inisialisasi stack.
        """
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)

    def test_push(self):
        """
        Test operasi push.
        """
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), 10)

        self.stack.push(20)
        self.assertEqual(self.stack.size(), 2)
        self.assertEqual(self.stack.peek(), 20)

    def test_pop(self):
        """
        Test operasi pop.
        """
        self.stack.push('a')
        self.stack.push('b')
        
        popped_item = self.stack.pop()
        self.assertEqual(popped_item, 'b')
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), 'a')

        popped_item = self.stack.pop()
        self.assertEqual(popped_item, 'a')
        self.assertEqual(self.stack.size(), 0)
        self.assertTrue(self.stack.is_empty())

    def test_pop_from_empty_stack(self):
        """
        Test pop dari stack kosong, harus menimbulkan IndexError.
        """
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek(self):
        """
        Test operasi peek.
        """
        self.stack.push(100)
        self.stack.push(200)

        peeked_item = self.stack.peek()
        self.assertEqual(peeked_item, 200)
        self.assertEqual(self.stack.size(), 2) 

    def test_peek_from_empty_stack(self):
        """
        Test peek dari stack kosong, harus menimbulkan IndexError.
        """
        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_is_empty(self):
        """
        Test operasi is_empty.
        """
        self.assertTrue(self.stack.is_empty())
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    def test_size(self):
        """
        Test operasi size.
        """
        self.assertEqual(self.stack.size(), 0)
        self.stack.push('satu')
        self.assertEqual(self.stack.size(), 1)
        self.stack.push('dua')
        self.assertEqual(self.stack.size(), 2)
        self.stack.pop()
        self.assertEqual(self.stack.size(), 1)
        self.stack.pop()
        self.assertEqual(self.stack.size(), 0)

if __name__ == '__main__':
    unittest.main()
