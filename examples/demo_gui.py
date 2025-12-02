import sys
import os
import tkinter as tk
from tkinter import messagebox

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from mesin.penggabung import TextEditorEngine

class EditorGUI:
    def __init__(self, root):
        self.engine = TextEditorEngine()
        self.root = root
        self.root.title("Text Editor Struktur Data")
        
        # Text Area
        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(pady=10)
        self.text_area.bind('<KeyRelease>', self.on_key_release)

        # Tombol Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Undo", command=self.do_undo).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Redo", command=self.do_redo).pack(side=tk.LEFT, padx=5)

        # Label Saran
        self.lbl_saran = tk.Label(root, text="Saran Autocomplete: -", fg="blue")
        self.lbl_saran.pack(pady=5)

        # Variabel helper untuk melacak perubahan manual vs undo/redo
        self.ignore_change = False

    def on_key_release(self, event):
        if self.ignore_change:
            return
            
        # Tombol navigasi/khusus tidak dianggap pengetikan konten baru
        if event.keysym in ['Return', 'BackSpace', 'space'] or len(event.char) == 1:
             current_text = self.text_area.get("1.0", tk.END).strip()
             
             # Logika sederhana: simpan setiap spasi (kata selesai) atau enter
             # Untuk implementasi real-time yang sempurna butuh logika diff yang kompleks,
             # ini versi simplifikasi: setiap pengetikan dianggap write baru jika berbeda.
             # (Di proyek nyata, biasanya trigger save state per kata / timer)
             pass 

        # Cek autocomplete untuk kata terakhir
        full_text = self.text_area.get("1.0", "end-1c")
        words = full_text.split()
        if words:
            last_word = words[-1]
            suggestions = self.engine.get_suggestions(last_word)
            self.lbl_saran.config(text=f"Saran Autocomplete: {', '.join(suggestions)}")
        
    def save_current_state(self, event=None):
        # Fungsi ini bisa dipanggil manual atau via bind 'space' untuk menyimpan state
        pass

    # Untuk demo sederhana, kita gunakan tombol Write Manual agar logika Undo jelas
    # karena menangkap event 'tiap ketik' di GUI untuk undo/redo agak kompleks tanpa library diff.
    
    # --- REVISI PENDEKATAN GUI SEDERHANA ---
    # Agar sesuai dengan logika engine (write per blok), kita buat input field dan display field
    
def run_gui_simple():
    """GUI Sederhana: Input di bawah, Tampilan Utama di atas"""
    root = tk.Tk()
    root.title("Demo GUI Editor")
    
    engine = TextEditorEngine()
    
    lbl_display = tk.Label(root, text="Dokumen:", font=("Arial", 12, "bold"))
    lbl_display.pack()
    
    display = tk.Label(root, text="(Kosong)", bg="white", width=50, height=10, relief="sunken", anchor="nw", justify="left")
    display.pack(padx=10, pady=5)
    
    lbl_input = tk.Label(root, text="Ketik tambahan teks di sini:")
    lbl_input.pack()
    
    entry_input = tk.Entry(root, width=40)
    entry_input.pack(pady=5)
    
    lbl_saran = tk.Label(root, text="Saran: -", fg="blue")
    lbl_saran.pack()

    def update_display():
        display.config(text=engine.get_content())

    def on_submit(event=None):
        text = entry_input.get()
        if text:
            engine.write(text + " ") # Tambah spasi otomatis
            entry_input.delete(0, tk.END)
            update_display()

    def on_type(event):
        # Cek saran realtime
        current = entry_input.get()
        if current:
            saran = engine.get_suggestions(current.split()[-1])
            lbl_saran.config(text=f"Saran: {', '.join(saran)}")
        else:
            lbl_saran.config(text="Saran: -")

    def do_undo():
        engine.undo()
        update_display()
        
    def do_redo():
        engine.redo()
        update_display()

    entry_input.bind("<Return>", on_submit)
    entry_input.bind("<KeyRelease>", on_type)
    
    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=10)
    
    tk.Button(frame_btn, text="Tambah Teks (Enter)", command=on_submit).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Undo", command=do_undo, bg="#ffcccc").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Redo", command=do_redo, bg="#ccffcc").pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    run_gui_simple()