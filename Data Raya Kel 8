import tkinter as tk
import random

class TebakAngkaBomGUI:
    def __init__(self, root):
        self.angka_bom = random.randint(1, 100)
        self.batas_bawah = 1
        self.batas_atas = 100

        root.title("Tebak Angka Bom")
        root.geometry("400x200")

        self.judul = tk.Label(root, text="Tebak angka (1-100), Hindari BOM!", font=("Arial", 12))
        self.judul.pack(pady=5)

        self.input_tebakan = tk.Entry(root, font=("Arial", 12))
        self.input_tebakan.pack(pady=5)

        self.tombol_tebak = tk.Button(root, text="Tebak", font=("Arial", 12), command=self.cek_tebakan)
        self.tombol_tebak.pack(pady=5)

        self.label_info = tk.Label(root, text="Masukkan angka antara 1 dan 100", font=("Arial", 12))
        self.label_info.pack(pady=5)

    def cek_tebakan(self):
        try:
            tebakan = int(self.input_tebakan.get())

            if tebakan < self.batas_bawah or tebakan > self.batas_atas:
                self.label_info.config(text=f"Tebakan harus antara {self.batas_bawah} dan {self.batas_atas}!")
                return

            if tebakan == self.angka_bom:
                self.label_info.config(text=f"💥 BOOM! Kamu kalah! Angka bom: {self.angka_bom}")
                self.tombol_tebak.config(state="disabled")
            elif tebakan < self.angka_bom:
                self.batas_bawah = tebakan + 1
                self.label_info.config(text=f"Aman! Tebak lagi antara {self.batas_bawah} dan {self.batas_atas}")
            else:
                self.batas_atas = tebakan - 1
                self.label_info.config(text=f"Aman! Tebak lagi antara {self.batas_bawah} dan {self.batas_atas}")

            self.input_tebakan.delete(0, tk.END)

        except ValueError:
            self.label_info.config(text="Masukkan angka yang valid!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TebakAngkaBomGUI(root)
    root.mainloop()
