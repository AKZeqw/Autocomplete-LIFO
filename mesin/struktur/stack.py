"""
File: stack.py

Class wrapper sederhana untuk struktur data Stack menggunakan list Python.
"""

class Stack:
    """
    Kelas implementasi struktur data Stack (Tumpukan).

    Menggunakan list bawaan Python sebagai penyimpan data internal,
    dengan operasi dasar LIFO (Last-In, First-Out).
    """
    def __init__(self):
        self._items = []

    def push(self, item):
        """
        Menambahkan item baru ke atas (top) dari stack.
        :param item: Item yang akan ditambahkan.
        """
        self._items.append(item)

    def pop(self):
        """
        Menghapus dan mengembalikan item teratas dari stack.
        Jika stack kosong, akan menimbulkan IndexError.
        :return: Item teratas dari stack.
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """
        Mengembalikan item teratas dari stack tanpa menghapusnya.
        Jika stack kosong, akan menimbulkan IndexError.
        :return: Item teratas dari stack.
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        """
        Memeriksa apakah stack kosong.
        :return: True jika stack kosong, False jika sebaliknya.
        """
        return len(self._items) == 0

    def size(self):
        """
        Mengembalikan jumlah item dalam stack.
        :return: Integer yang merepresentasikan jumlah item.
        """
        return len(self._items)
