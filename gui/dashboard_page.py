import tkinter as tk
from tkinter import ttk, messagebox

# Untuk mendapatkan saldo & rekening, kita cukup akses object nasabah
# yang sudah disimpan saat login.

class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label_title = ttk.Label(self, text="Dashboard", font=("Segoe UI", 18, "bold"))
        self.label_title.pack(pady=20)

        # Informasi nasabah
        self.label_nama = ttk.Label(self, text="Nama: -", font=("Segoe UI", 12))
        self.label_nama.pack(pady=5)

        self.label_nomor_rekening = ttk.Label(self, text="Nomor Rekening: -", font=("Segoe UI", 12))
        self.label_nomor_rekening.pack(pady=5)

        self.label_saldo = ttk.Label(self, text="Saldo: -", font=("Segoe UI", 12))
        self.label_saldo.pack(pady=5)

        # Tombol transfer
        ttk.Button(
            self,
            text="Transfer",
            width=25,
            command=lambda: controller.show_frame("TransferPage")
        ).pack(pady=10)

        # Tombol Deposit & Withdraw
        ttk.Button(
            self,
            text="Deposit / Withdraw",
            width=25,
            command=lambda: controller.show_frame("TransaksiPage")
        ).pack(pady=10)

        # Tombol logout
        ttk.Button(
            self,
            text="Logout", width=25,
            command=self.logout
        ).pack(pady=10)
        
        ttk.Button(
            self,
            text="Riwayat Transaksi",
            width=25,
            command=lambda: (
                controller.frames["RiwayatPage"].load_data(),
                controller.show_frame("RiwayatPage")
            )
        ).pack(pady=10)


    def tkraise(self, *args, **kwargs):
        """Override tkraise supaya data user di-refresh setiap kali halaman muncul"""
        try:
            user = self.controller.current_user
            rekening = user.rekening  # langsung dapat object rekening
            self.label_nama.config(text=f"Nama: {user.nama}")
            self.label_nomor_rekening.config(text=f"Nomor Rekening: {rekening.nomor_rekening}")
            self.label_saldo.config(text=f"Saldo: {rekening.jumlah_saldo}")
        except:
            pass

        super().tkraise(*args, **kwargs)

    def logout(self):
        confirm = messagebox.askyesno(
        "Logout",
        "Apakah Anda yakin ingin logout dari akun ini?"
        )

        if not confirm:
            return

        # Hapus user dari aplikasi
        self.controller.current_user = None

        # Bersihkan input login saat kembali ke halaman login
        login_page = self.controller.frames["LoginPage"]
        login_page.entry_phone.delete(0, tk.END)
        login_page.entry_password.delete(0, tk.END)

        messagebox.showinfo("Logout", "Anda berhasil logout.")
        self.controller.show_frame("LoginPage")

