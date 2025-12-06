import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Import fungsi helper sesuai aturan Abet
from database_interface.manager import transfer
from database_interface.helper import nomor_rekening_ke_Rekening


class TransferPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="Transfer Uang", font=("Segoe UI", 18, "bold"))
        title.pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Nomor Rekening Tujuan:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_rek_tujuan = ttk.Entry(form, width=30)
        self.entry_rek_tujuan.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Jumlah Uang:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_jumlah = ttk.Entry(form, width=30)
        self.entry_jumlah.grid(row=1, column=1, pady=5)

        ttk.Button(self, text="Kirim", command=self.do_transfer).pack(pady=15)

        ttk.Button(self, text="Kembali ke Dashboard",
                   command=lambda: controller.show_frame("DashboardPage")
                   ).pack()

    def do_transfer(self):
        user = self.controller.current_user
        rekening_sumber = self.controller.selected_rekening

        rek_tujuan_no = self.entry_rek_tujuan.get().strip()
        jumlah_str = self.entry_jumlah.get().strip()

        if not rek_tujuan_no or not jumlah_str:
            messagebox.showerror("Error", "Semua field harus diisi")
            return

        try:
            jumlah = int(jumlah_str)
            if jumlah <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Jumlah uang harus berupa angka positif")
            return

        try:
            rekening_tujuan = nomor_rekening_ke_Rekening(rek_tujuan_no)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Gagal menemukan rekening tujuan: {str(e)}")
            return

        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            transfer(jumlah, waktu, rekening_sumber, rekening_tujuan)
        except Exception as e:
            messagebox.showerror("Gagal", e.args[0]['message'])
            return

        messagebox.showinfo("Sukses", "Transfer berhasil!")

        self.entry_rek_tujuan.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)

        self.controller.show_frame("DashboardPage")
