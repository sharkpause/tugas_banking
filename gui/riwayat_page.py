import tkinter as tk
from tkinter import ttk, messagebox

from database_interface.manager import fetch_riwayat_transaksi


class RiwayatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Riwayat Transaksi", font=("Arial", 20, "bold")).pack(pady=10)

        columns = ("tanggal", "jenis", "jumlah", "sumber", "tujuan")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.heading("tanggal", text="Tanggal")
        self.tree.heading("jenis", text="Jenis")
        self.tree.heading("jumlah", text="Jumlah")
        self.tree.heading("sumber", text="Rek Sumber")
        self.tree.heading("tujuan", text="Rek Tujuan")

        self.tree.column("tanggal", width=160)
        self.tree.column("jenis", width=90)
        self.tree.column("jumlah", width=100)
        self.tree.column("sumber", width=130)
        self.tree.column("tujuan", width=130)

        self.tree.pack(padx=20, pady=10)

        self.label_total_masuk = tk.Label(
            self, text="Total Uang Masuk: -", font=("Arial", 12)  
        )
        self.label_total_masuk.pack(pady=(5, 0))

        self.label_total_keluar = tk.label(
            self, text="Total Uang Keluar: -",font=("Arial", 12)
        )
        self.label_total_keluar.pack(pady=(0, 10))


        ttk.Button(
            self,
            text="Kembali ke Dashboard",
            width=25,
            command=lambda: controller.show_frame("DashboardPage")
        ).pack(pady=10)

    def load_data(self):
        rekening = self.controller.current_user.rekening

        if rekening is None:
            messagebox.showerror("Error", "Rekening tidak ditemukan.")
            return

        nomor_rekening = rekening.nomor_rekening

        try:
            riwayat = fetch_riwayat_transaksi(nomor_rekening)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil riwayat transaksi:\n{e}")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for t in riwayat:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    t.datetime_transaksi,
                    t.jenis_transaksi,
                    t.jumlah_uang,
                    t.nomor_rekening_sumber,
                    t.nomor_rekening_tujuan
                )
            )
        
        total_masuk = 0
        total_keluar = 0

        for t in riwayat:
            
            if t.nomor_rekening_tujuan == nomor_rekening:
                total_masuk += t.jumlah_uang

            if t.nomor_rekening_sumber == nomor_rekening:
                total_keluar += t.jumlah_uang

            if t.jenis_transaksi.lower() == "deposit":
                total_masuk += t.jumlah_uang

            if t.jenis_transaksi.lower() == "withdraw":
                total_keluar += t.jumlah_uang
     
        self.label_total_masuk.config(text=f"Total Uang Masuk: {total_masuk}")
        self.label_total_keluar.config(text=f"Total Uang Keluar: {total_keluar}")