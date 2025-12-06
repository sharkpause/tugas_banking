import tkinter as tk
from tkinter import ttk, messagebox
from enum import IntEnum
from datetime import datetime

from database_interface.manager import fetch_aliran_uang
from .utils.currency import indo

class Row(IntEnum):
    TITLE = 0
    NAMA = 1
    NOMOR_REKENING = 2
    SALDO = 3
    BULAN_MASUK = 4
    BULAN_KELUAR = 5

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

        ttk.Label(info, text='Income:', font=("Segoe UI", 12), foreground="#2ecc71").grid(
            row=Row.BULAN_MASUK, column=Column.TITLE, sticky='w', pady=(15, 0)
        )
        self.label_bulan_masuk = ttk.Label(info, text="0", font=("Segoe UI", 12), foreground="#2ecc71")
        self.label_bulan_masuk.grid(
            row=Row.BULAN_MASUK, column=Column.DATA, sticky='w',
            padx=(15, 0), pady=(15, 0)
        )

        ttk.Label(info, text='Expense:', font=("Segoe UI", 12), foreground="#e67e22").grid(
            row=Row.BULAN_KELUAR, column=Column.TITLE, sticky='w'
        )
        self.label_bulan_keluar = ttk.Label(info, text="0", font=("Segoe UI", 12), foreground="#e67e22")
        self.label_bulan_keluar.grid(
            row=Row.BULAN_KELUAR, column=Column.DATA, sticky='w',
            padx=(15, 0)
        )

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
            text="Pilih rekening lain", width=25,
            command=self.pilih_rekening_lain
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

    def pilih_rekening_lain(self):
        self.controller.selected_rekening = None

        self.controller.show_frame('PilihRekeningPage')

    def tkraise(self, *args, **kwargs):
        try:
            user = self.controller.current_user
            rekening = self.controller.selected_rekening

            self.label_nama.config(text=f"{user.nama}")
            self.label_nomor_rekening.config(text=f"{rekening.nomor_rekening}")

            saldo_text = f'Rp{rekening.jumlah_saldo:,.2f}'
            saldo_text = saldo_text.replace(',', '_').replace('.', ',').replace('_', '.')
            self.label_saldo.config(text=saldo_text)

            aliran_uang = fetch_aliran_uang(rekening.nomor_rekening)

            current_month = datetime.now().strftime('%Y-%m')
            current_month_flow = aliran_uang.get(current_month, {
                'total_uang_masuk': 0,
                'total_uang_keluar': 0
            })

            self.label_bulan_masuk.config(text=str(indo(current_month_flow['total_uang_masuk'])))
            self.label_bulan_keluar.config(text=str(indo(current_month_flow['total_uang_keluar'])))
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        super().tkraise(*args, **kwargs)

    def logout(self):
        confirm = messagebox.askyesno(
        "Logout",
        "Apakah Anda yakin ingin logout dari akun ini?"
        )

        if not confirm:
            return

        self.controller.current_user = None
        self.controller.selected_rekening = None

        login_page = self.controller.frames["LoginPage"]
        login_page.entry_phone.delete(0, tk.END)
        login_page.entry_password.delete(0, tk.END)

        messagebox.showinfo("Logout", "Anda berhasil logout.")
        self.controller.show_frame("LoginPage")

