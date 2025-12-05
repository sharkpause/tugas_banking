import tkinter as tk
from tkinter import ttk, messagebox

# Import fungsi buat nasabah baru sesuai aturan Abet
from database_interface.manager import buat_nasabah_baru
from database_interface.CustomClasses import ValidationError

class RegisterPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="Daftar Akun Nasabah", font=("Segoe UI", 18, "bold"))
        title.pack(pady=20)

        # Frame form input
        form = ttk.Frame(self)
        form.pack(pady=10)

        # Nama lengkap
        ttk.Label(form, text="Nama Lengkap:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nama = ttk.Entry(form, width=30)
        self.entry_nama.grid(row=0, column=1, pady=5)

        # Email
        ttk.Label(form, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(form, width=30)
        self.entry_email.grid(row=1, column=1, pady=5)

        # Nomor telepon
        ttk.Label(form, text="Nomor Telepon:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_phone = ttk.Entry(form, width=30)
        self.entry_phone.grid(row=2, column=1, pady=5)

        # Alamat
        ttk.Label(form, text="Alamat:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_alamat = ttk.Entry(form, width=30)
        self.entry_alamat.grid(row=3, column=1, pady=5)

        # Password
        ttk.Label(form, text="Password:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_password = ttk.Entry(form, width=30, show="*")
        self.entry_password.grid(row=4, column=1, pady=5)

        # Tombol daftar
        ttk.Button(self, text="Daftar", command=self.do_register).pack(pady=15)

        # Tombol kembali ke login
        ttk.Button(self, text="Kembali ke Login",
                   command=lambda: controller.show_frame("LoginPage")
                   ).pack()

    def do_register(self):
        nama = self.entry_nama.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()
        alamat = self.entry_alamat.get().strip()
        password = self.entry_password.get().strip()

        if not all([nama, email, phone, alamat, password]):
            messagebox.showerror("Error", "Semua field harus diisi")
            return

        try:
            nasabah = buat_nasabah_baru(
                nama=nama,
                password=password,
                email=email,
                nomor_telepon=phone,
                alamat=alamat
            )
            messagebox.showinfo("Sukses", "Akun berhasil dibuat. Silakan login.")
            self.controller.show_frame("LoginPage")
        except ValidationError as e:
            fields = e.errors['errors']
            msg = ''

            for field in fields:
                msg += field['message'] + '\n'
            messagebox.showerror("Gagal", msg)
        except Exception as e:
            messagebox.showerror("Gagal", str(e))
            return
