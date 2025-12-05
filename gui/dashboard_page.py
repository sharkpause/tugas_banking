import tkinter as tk
from tkinter import ttk, messagebox
from enum import IntEnum

class Row(IntEnum):
    TITLE = 0
    NAMA = 10
    NOMOR_REKENING = 20
    SALDO = 30

class Column(IntEnum):
    TITLE = 0
    DATA = 1

class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        info = ttk.Frame(self)
        info.pack(pady=10)

        title_frame = ttk.Frame(info, padding=(0, 0, 0, 25))
        title_frame.grid(row=Row.TITLE, column=Column.TITLE, columnspan=2)
        self.label_title = ttk.Label(title_frame, text="Dashboard", font=("Segoe UI", 18, "bold"))
        self.label_title.pack()

        ttk.Label(info, text="Nama:", font=("Segoe UI", 12)).grid(
            row=Row.NAMA, column=Column.TITLE, sticky='w', pady=(15, 0)
        )
        self.label_nama = ttk.Label(info, text='-', font=('Segoe UI', 12))
        self.label_nama.grid(row=Row.NAMA, column=Column.DATA, sticky='w', padx=(15, 0))

        ttk.Label(info, text="Nomor Rekening:", font=("Segoe UI", 12)).grid(
            row=Row.NOMOR_REKENING, column=Column.TITLE, sticky='w'
        )
        self.label_nomor_rekening = ttk.Label(info, text='-', font=('Segoe UI', 12))
        self.label_nomor_rekening.grid(row=Row.NOMOR_REKENING, column=Column.DATA, sticky='w', padx=(15, 0))

        ttk.Label(info, text="Saldo:", font=("Segoe UI", 12)).grid(
            row=Row.SALDO, column=Column.TITLE, sticky='w'
        )
        self.label_saldo = ttk.Label(info, text='-', font=('Segoe UI', 12))
        self.label_saldo.grid(row=Row.SALDO, column=Column.DATA, sticky='w', padx=(15, 0))

        ttk.Button(
            self,
            text="Transfer",
            width=25,
            command=lambda: controller.show_frame("TransferPage")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Deposit / Withdraw",
            width=25,
            command=lambda: controller.show_frame("TransaksiPage")
        ).pack(pady=10)

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

        self.label_pemasukan = ttk.Label(self, text="Pemasukan bulan ini: -", font=("Segoe UI", 12))
        self.label_pemasukan.pack(pady=5)

        self.label_pengeluaran = ttk.Label(self, text="Pengeluaran bulan ini: -", font=("Segoe UI", 12))
        self.label_pengeluaran.pack(pady=5)


    def tkraise(self, *args, **kwargs):
        try:
            user = self.controller.current_user
            rekening = user.rekening  

            self.label_nama.config(text=f"{user.nama}")
            self.label_nomor_rekening.config(text=f"{rekening.nomor_rekening}")
            self.label_saldo.config(text=f"{rekening.jumlah_saldo}")

            try:
                pemasukan = rekening.hitung_pemasukan_bulan_ini()
                pengeluaran = rekening.hitung_pengeluaran_bulan_ini()

                self.label_pemasukan.config(text=f"Pemasukan bulan ini: {pemasukan}")
                self.label_pengeluaran.config(text=f"Pengeluaran bulan ini: {pengeluaran}")
            except:
                self.label_pemasukan.config(text="Pemasukan bulan ini: -")
                self.label_pengeluaran.config(text="Pengeluaran bulan ini: -")

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

        self.controller.current_user = None

        login_page = self.controller.frames["LoginPage"]
        login_page.entry_phone.delete(0, tk.END)
        login_page.entry_password.delete(0, tk.END)

        messagebox.showinfo("Logout", "Anda berhasil logout.")
        self.controller.show_frame("LoginPage")

