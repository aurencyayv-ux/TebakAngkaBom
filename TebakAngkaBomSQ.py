import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import pandas as pd
import sqlite3
import os

class TebakAngkaBomGUI:
    def __init__(self, root):
        self.db_name = "tebakan.db"
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

        self.angka_bom = random.randint(1, 100)
        self.batas_bawah = 1
        self.batas_atas = 100

        root.title("🎯 Tebak Angka Bom")
        root.geometry("600x400")

        self.judul = tk.Label(root, text="Tebak angka (1–100), Hindari BOM!", font=("Arial", 12))
        self.judul.pack(pady=5)

        self.input_tebakan = tk.Entry(root, font=("Arial", 12))
        self.input_tebakan.pack(pady=5)

        self.tombol_tebak = tk.Button(root, text="Tebak", font=("Arial", 12), command=self.cek_tebakan)
        self.tombol_tebak.pack(pady=5)

        self.label_info = tk.Label(root, text="Masukkan angka antara 1 dan 100", font=("Arial", 12))
        self.label_info.pack(pady=5)

        frame_btn = tk.Frame(root)
        frame_btn.pack(pady=10)

        self.btn_export = tk.Button(frame_btn, text="Export Excel", command=self.export_excel)
        self.btn_export.grid(row=0, column=0, padx=10)

        self.btn_import = tk.Button(frame_btn, text="Import Excel", command=self.import_excel)
        self.btn_import.grid(row=0, column=1, padx=10)

        self.btn_refresh = tk.Button(frame_btn, text="Refresh Data", command=self.tampilkan_data)
        self.btn_refresh.grid(row=0, column=2, padx=10)

        self.btn_reset = tk.Button(root, text="Mulai Ulang Game", command=self.reset_game)
        self.btn_reset.pack(pady=5)

        # ====== Tambahkan Treeview untuk menampilkan isi data ======
        self.tree = ttk.Treeview(root, columns=("id", "tebakan", "batas_bawah", "batas_atas", "hasil"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("tebakan", text="Tebakan")
        self.tree.heading("batas_bawah", text="Batas Bawah")
        self.tree.heading("batas_atas", text="Batas Atas")
        self.tree.heading("hasil", text="Hasil")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tampilkan_data()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS riwayat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tebakan INTEGER,
                batas_bawah INTEGER,
                batas_atas INTEGER,
                hasil TEXT
            )
        """)
        self.conn.commit()

    def cek_tebakan(self):
        try:
            tebakan = int(self.input_tebakan.get())

            if tebakan < self.batas_bawah or tebakan > self.batas_atas:
                self.label_info.config(text=f"Tebakan harus antara {self.batas_bawah} dan {self.batas_atas}!")
                return

            if tebakan == self.angka_bom:
                hasil = "Kalah (kena bom)"
                self.label_info.config(text=f"💥 BOOM! Kamu kalah! Angka bom: {self.angka_bom}")
                self.tombol_tebak.config(state="disabled")
            elif tebakan < self.angka_bom:
                self.batas_bawah = tebakan + 1
                hasil = "Aman"
                self.label_info.config(text=f"Aman! Tebak lagi antara {self.batas_bawah} dan {self.batas_atas}")
            else:
                self.batas_atas = tebakan - 1
                hasil = "Aman"
                self.label_info.config(text=f"Aman! Tebak lagi antara {self.batas_bawah} dan {self.batas_atas}")

            self.save_to_db(tebakan, self.batas_bawah, self.batas_atas, hasil)
            self.tampilkan_data()
            self.input_tebakan.delete(0, tk.END)

        except ValueError:
            self.label_info.config(text="Masukkan angka yang valid!")

    def save_to_db(self, tebakan, batas_bawah, batas_atas, hasil):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO riwayat (tebakan, batas_bawah, batas_atas, hasil) VALUES (?, ?, ?, ?)",
            (tebakan, batas_bawah, batas_atas, hasil)
        )
        self.conn.commit()

    def tampilkan_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM riwayat")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def export_excel(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM riwayat")
        rows = cursor.fetchall()

        if not rows:
            messagebox.showwarning("Peringatan", "Belum ada data untuk diexport!")
            return

        df = pd.DataFrame(rows, columns=["ID", "Tebakan", "Batas Bawah", "Batas Atas", "Hasil"])

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Sukses", f"Data berhasil disimpan ke {file_path}")

    def import_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            required_cols = {"Tebakan", "Batas Bawah", "Batas Atas", "Hasil"}

            if not required_cols.issubset(df.columns):
                messagebox.showerror("Error", f"Kolom Excel tidak sesuai! Harus mengandung: {required_cols}")
                return

            cursor = self.conn.cursor()
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO riwayat (tebakan, batas_bawah, batas_atas, hasil) VALUES (?, ?, ?, ?)",
                    (int(row["Tebakan"]), int(row["Batas Bawah"]), int(row["Batas Atas"]), str(row["Hasil"]))
                )
            self.conn.commit()

            messagebox.showinfo("Sukses", f"Berhasil impor {len(df)} baris data dari Excel!")
            self.tampilkan_data()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file Excel:\n{e}")

    def reset_game(self):
        self.angka_bom = random.randint(1, 100)
        self.batas_bawah = 1
        self.batas_atas = 100
        self.label_info.config(text="Game baru dimulai! Masukkan angka antara 1 dan 100")
        self.tombol_tebak.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = TebakAngkaBomGUI(root)
    root.mainloop()
