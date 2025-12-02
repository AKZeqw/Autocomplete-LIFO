import sys
import os

# Menambahkan root directory ke sys.path agar bisa import module 'mesin'
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from mesin.penggabung import TextEditorEngine

def run_cli():
    editor = TextEditorEngine()
    print("=== Demo CLI Text Editor ===")
    print("Ketik teks untuk menulis.")
    print("Perintah khusus: 'undo', 'redo', 'show', 'exit'")
    print("--------------------------------------------------")

    while True:
        # .strip() menghapus spasi di awal/akhir input
        original_input = input(">> ")
        clean_input = original_input.strip().lower()
        
        if clean_input == 'exit':
            break
            
        # Sekarang menerima 'undo' ATAU ':undo' agar lebih fleksibel
        elif clean_input in ['undo', ':undo']:
            if editor.undo():
                print(f"[Undo Berhasil]") 
                # Otomatis show content setelah undo
                print(f"Isi Dokumen: {editor.get_content()}")
            else:
                print("[Undo Gagal] Tidak ada riwayat aksi sebelumnya.")
                
        elif clean_input in ['redo', ':redo']:
            if editor.redo():
                print(f"[Redo Berhasil]")
                print(f"Isi Dokumen: {editor.get_content()}")
            else:
                print("[Redo Gagal] Tidak ada riwayat undo yang bisa diulang.")
                
        elif clean_input in ['show', ':show']:
            print(f"Isi Dokumen: {editor.get_content()}")
            
        elif clean_input.startswith('saran ') or clean_input.startswith(':saran '):
            # Ambil kata setelah perintah 'saran'
            prefix = clean_input.split(' ', 1)[1]
            print(f"Saran untuk '{prefix}': {editor.get_suggestions(prefix)}")
            
        else:
            # Jika bukan perintah, anggap sebagai tulisan
            # Gunakan original_input agar spasi/huruf besar user terjaga
            editor.write(original_input + " ")
            print(f"Konten saat ini: {editor.get_content()}")
            
            # Cek saran otomatis untuk kata terakhir yang diketik
            words = original_input.split()
            if words:
                last_word = words[-1]
                saran = editor.get_suggestions(last_word)
                if saran:
                    print(f"(Autocomplete tersedia: {', '.join(saran)})")

if __name__ == "__main__":
    run_cli()