import tkinter as tk
from tkinter import ttk, messagebox

from database_interface.manager import login_nasabah

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="Login Nasabah", font=("Segoe UI", 18, "bold"))
        title.pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Nomor Telepon:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_phone = ttk.Entry(form, width=30)
        self.entry_phone.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_password = ttk.Entry(form, width=30, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        self.showing = False
        self.toggle_btn = ttk.Button(form, text="Show", command=self.toggle_password)
        self.toggle_btn.grid(row=1, column=2, pady=5)

        btn_login = ttk.Button(self, text="Login", command=self.login)
        btn_login.pack(pady=15)

        ttk.Button(self, text="Daftar Akun Baru",
            command=lambda: controller.show_frame("RegisterPage")
        ).pack()

        ttk.Button(controller, text="Login sebagai admin", bootstyle='dark',
            command=lambda: controller.show_frame("AdminPage")
        ).place(relx=1.0, y=15, x=-15, anchor='ne')

    def toggle_password(self):
        if self.showing:
            self.showing = False
            self.entry_password.config(show='*')
            self.toggle_btn.config(text="Show")
        else:
            self.showing = True
            self.entry_password.config(show='')
            self.toggle_btn.config(text="Hide")

    def login(self):
        phone = self.entry_phone.get().strip()
        password = self.entry_password.get().strip()

        if not phone or not password:
            messagebox.showerror("Error", "Semua field harus diisi")
            return

        try:
            result = login_nasabah(phone, password)  
        except Exception as e:
            messagebox.showerror("Login gagal", e.args[0]['message'])
            return

        self.controller.current_user = result['object']

        messagebox.showinfo("Sukses", f"Selamat datang, {self.controller.current_user.nama}!")
        self.controller.show_frame("PilihRekeningPage")
