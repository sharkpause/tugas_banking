import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database_interface.manager import deposit, withdraw


class TransaksiPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="Deposit & Withdraw", font=("Segoe UI", 18, "bold"))
        title.pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Jumlah Uang:").grid(row=0, column=0, pady=10, sticky="w")
        self.entry_jumlah = ttk.Entry(form, width=30)
        self.entry_jumlah.grid(row=0, column=1, pady=10)

        # Tombol Deposit dan Withdraw
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Deposit", width=15, command=self.do_deposit).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Withdraw", width=15, command=self.do_withdraw).grid(row=0, column=1, padx=10)

        # Kembali ke Dashboard
        ttk.Button(self, text="Kembali ke Dashboard",
                   command=lambda: controller.show_frame("DashboardPage")
                   ).pack(pady=15)

    def get_amount(self):
        """Helper untuk mengambil input jumlah dengan validasi."""
        jumlah_str = self.entry_jumlah.get().strip()
        if not jumlah_str:
            messagebox.showerror("Error", "Jumlah uang tidak boleh kosong")
            return None

        try:
            jumlah = int(jumlah_str)
            if jumlah <= 0:
                raise ValueError
            return jumlah
        except:
            messagebox.showerror("Error", "Jumlah harus berupa angka positif")
            return None

    def do_deposit(self):
        user = self.controller.current_user
        rekening = user.rekening

        jumlah = self.get_amount()
        if jumlah is None:
            return

        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            deposit(jumlah, waktu, rekening)
        except Exception as e:
            messagebox.showerror("Gagal", str(e))
            return

        messagebox.showinfo("Sukses", "Deposit berhasil!")

        self.entry_jumlah.delete(0, tk.END)
        self.controller.show_frame("DashboardPage")

    def do_withdraw(self):
        user = self.controller.current_user
        rekening = user.rekening

        jumlah = self.get_amount()
        if jumlah is None:
            return

        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            withdraw(jumlah, waktu, rekening)
        except Exception as e:
            messagebox.showerror("Gagal", str(e))
            return

        messagebox.showinfo("Sukses", "Withdraw berhasil!")

        self.entry_jumlah.delete(0, tk.END)
        self.controller.show_frame("DashboardPage")
