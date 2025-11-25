import tkinter as tk
from tkinter import ttk, messagebox

# Import fungsi login dari database_interface (aman sesuai aturan)
from database_interface.manager import login_nasabah

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Judul
        title = ttk.Label(self, text="Login Nasabah", font=("Segoe UI", 18, "bold"))
        title.pack(pady=20)

        # Frame untuk input
        form = ttk.Frame(self)
        form.pack(pady=10)

        # Nomor telepon
        ttk.Label(form, text="Nomor Telepon:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_phone = ttk.Entry(form, width=30)
        self.entry_phone.grid(row=0, column=1, pady=5)

        # Password
        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_password = ttk.Entry(form, width=30, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        # Tombol login
        btn_login = ttk.Button(self, text="Login", command=self.login)
        btn_login.pack(pady=15)

        # Tombol ke register
        ttk.Button(self, text="Daftar Akun Baru",
                   command=lambda: controller.show_frame("RegisterPage")
                   ).pack()

    def login(self):
        phone = self.entry_phone.get().strip()
        password = self.entry_password.get().strip()

        if not phone or not password:
            messagebox.showerror("Error", "Semua field harus diisi")
            return

        try:
            nasabah = login_nasabah(phone, password)   # <- panggil helper Abet
        except Exception as e:
            messagebox.showerror("Login gagal", str(e))
            return

        # Simpan object nasabah ke controller agar bisa dipakai halaman lain
        self.controller.current_user = nasabah

        messagebox.showinfo("Sukses", f"Selamat datang, {nasabah.nama}!")
        self.controller.show_frame("DashboardPage")
