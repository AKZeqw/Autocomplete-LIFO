from mesin.struktur.stack import Stack
from mesin.struktur.trie import Trie

class TextEditorEngine:
    def __init__(self):
        self.content = ""
        self.dictionary = Trie()
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        
        # Inisialisasi kamus dasar
        initial_words = ["apel", "aplikasi", "api", "bola", "balon", "belajar", "coding", "computer", "data", "struktur"]
        for word in initial_words:
            self.dictionary.insert(word)

    def write(self, text):
        """Menulis teks baru dan menyimpan state ke undo stack."""
        # Simpan state saat ini ke undo stack sebelum berubah
        self.undo_stack.push(self.content)
        
        # Saat ada aksi baru, redo stack harus di-reset karena history masa depan tidak valid
        self.redo_stack.clear()
        
        self.content += text
        
        # Tambahkan kata-kata baru ke Trie secara dinamis
        words = text.split()
        for word in words:
            clean_word = "".join(filter(str.isalpha, word)).lower()
            if clean_word:
                self.dictionary.insert(clean_word)

    def undo(self):
        """Membatalkan aksi terakhir."""
        if self.undo_stack.is_empty():
            return False # Gagal undo

        # Simpan state saat ini ke redo stack
        self.redo_stack.push(self.content)
        
        # Kembalikan konten dari undo stack
        self.content = self.undo_stack.pop()
        return True

    def redo(self):
        """Mengulangi aksi yang di-undo."""
        if self.redo_stack.is_empty():
            return False # Gagal redo

        # Simpan state saat ini ke undo stack
        self.undo_stack.push(self.content)
        
        # Ambil konten dari redo stack
        self.content = self.redo_stack.pop()
        return True

    def get_content(self):
        return self.content

    def get_suggestions(self, prefix):
        return self.dictionary.get_autocomplete_suggestions(prefix)