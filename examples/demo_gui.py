"""
File: demo_gui.py

Contoh implementasi dan demo GUI (Graphical User Interface)
menggunakan MesinKetik dengan pustaka Tkinter.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk

# -- Menambahkan parent directory ke sys.path untuk impor --
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ---------------------------------------------------------

from mesin.penggabung import MesinKetik

class App(tk.Tk):
    """
    Kelas utama untuk aplikasi GUI demo.
    """
    def __init__(self):
        super().__init__()

        # --- Konfigurasi Window ---
        self.title("Demo Autocomplete & Undo/Redo")
        self.geometry("800x600")

        # --- Inisialisasi MesinKetik ---
        file_kamus = os.path.join(parent_dir, 'data', 'kumpulan_kata.txt')
        self.mesin = MesinKetik(file_kamus)

        # --- Konfigurasi Style ---
        self.style = ttk.Style(self)
        self.style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'

        # --- Membuat Widget ---
        self._create_widgets()

        # --- Binding Events ---
        self._bind_events()
        
        # Inisialisasi state awal
        self.mesin.ketik(self.text_area.get("1.0", "end-1c"))

    def _create_widgets(self):
        """Membuat dan menata semua widget di window."""
        # Frame Utama
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Kolom Kiri (Editor Teks) ---
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Tombol Undo/Redo
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(0, 5))

        self.undo_button = ttk.Button(button_frame, text="Undo (Ctrl+Z)", command=self.handle_undo)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 5))

        self.redo_button = ttk.Button(button_frame, text="Redo (Ctrl+Y)", command=self.handle_redo)
        self.redo_button.pack(side=tk.LEFT)

        # Area Teks
        self.text_area = tk.Text(left_frame, wrap="word", font=("Helvetica", 12), undo=False)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # --- Kolom Kanan (Saran) ---
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(right_frame, text="Saran Autocomplete:", font=("Helvetica", 10, "bold")).pack(anchor="w")
        
        self.suggestion_listbox = tk.Listbox(right_frame, font=("Helvetica", 11))
        self.suggestion_listbox.pack(fill=tk.BOTH, expand=True)
        ttk.Label(right_frame, text="(Dobel-klik atau Tab untuk pilih)", font=("Helvetica", 8)).pack(anchor="w")


    def _bind_events(self):
        """Mendaftarkan semua event handler."""
        # Event setiap kali tombol keyboard dilepas di area teks
        self.text_area.bind("<KeyRelease>", self.handle_key_release)
        
        # Event untuk memilih saran dari listbox
        self.suggestion_listbox.bind("<Double-Button-1>", self.handle_suggestion_select)
        
        # Event untuk autocomplete dengan Tab dari area teks
        self.text_area.bind("<Tab>", self.handle_tab_complete)
        
        # Binding shortcut keyboard global
        self.bind_all("<Control-z>", lambda e: self.handle_undo())
        self.bind_all("<Control-y>", lambda e: self.handle_redo())

    def handle_key_release(self, event):
        """Handler saat pengguna mengetik di Text widget."""
        # Abaikan tombol spesial seperti Shift, Ctrl, Alt, Tab
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Tab"):
            return

        full_text = self.text_area.get("1.0", "end-1c")
        
        # Simpan state ke undo stack jika pengguna menekan spasi
        if event.keysym == "space":
            # Ambil teks sebelum spasi ditambahkan
            self.mesin.ketik(full_text.strip())
        
        # Dapatkan prefix kata di posisi kursor
        # 'insert' adalah posisi kursor saat ini
        cursor_pos = self.text_area.index(tk.INSERT)
        line, char = map(int, cursor_pos.split('.'))
        line_text = self.text_area.get(f"{line}.0", f"{line}.{char}")
        
        prefix = ""
        if line_text and not line_text.endswith(' '):
            prefix = line_text.split(' ')[-1]
            
        # Update saran di listbox
        self.update_suggestions(prefix)

    def handle_tab_complete(self, event):
        """Handler untuk autocomplete dengan tombol Tab."""
        if self.suggestion_listbox.size() > 0:
            # Ambil saran pertama (paling atas)
            selected_word = self.suggestion_listbox.get(0)
            self._complete_word(selected_word)
            return "break"  # Mencegah event Tab bawaan (fokus berpindah)
        # Jika tidak ada saran, biarkan default behavior Tab berjalan
        return

    def handle_undo(self):
        """Handler untuk aksi Undo."""
        new_text = self.mesin.undo()
        self.update_text_area(new_text)

    def handle_redo(self):
        """Handler untuk aksi Redo."""
        new_text = self.mesin.redo()
        self.update_text_area(new_text)

    def update_text_area(self, new_text):
        """Mengganti seluruh teks di Text widget dengan teks baru."""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", new_text)

    def _complete_word(self, selected_word):
        """
        Helper untuk mengganti kata/prefix saat ini dengan kata yang dipilih.
        """
        # Ganti prefix di Text widget dengan kata yang dipilih
        cursor_index = self.text_area.index(tk.INSERT)
        
        # Cari awal dari kata saat ini (prefix)
        # Mundur dari kursor sampai menemukan spasi atau awal baris
        start_of_word = self.text_area.search(r"\s", cursor_index, backwards=True, regexp=True)
        if not start_of_word:
            start_of_word = "1.0"
        else:
            # search mengembalikan posisi spasi, kita butuh posisi setelahnya
            start_of_word = self.text_area.index(f"{start_of_word}+1c")
            
        # Hapus prefix dan masukkan kata lengkap
        self.text_area.delete(start_of_word, tk.INSERT)
        self.text_area.insert(start_of_word, selected_word + " ") # Tambah spasi
        
        # Simpan state setelah autocomplete
        self.mesin.ketik(self.text_area.get("1.0", "end-1c").strip())
        self.update_suggestions("") # Kosongkan saran setelah dipilih

    def update_suggestions(self, prefix):
        """Memperbarui Listbox dengan saran kata baru."""
        self.suggestion_listbox.delete(0, tk.END)
        if prefix:
            saran = self.mesin.dapatkan_saran(prefix)
            for kata, freq in saran:
                self.suggestion_listbox.insert(tk.END, kata)

    def handle_suggestion_select(self, event):
        """Handler saat saran di Listbox dipilih (dobel-klik)."""
        selected_indices = self.suggestion_listbox.curselection()
        if not selected_indices:
            return
        selected_word = self.suggestion_listbox.get(selected_indices[0])
        self._complete_word(selected_word)

def main():
    """Fungsi utama untuk menjalankan aplikasi GUI."""
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
