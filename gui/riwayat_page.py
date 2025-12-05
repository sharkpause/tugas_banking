import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.ticker import MaxNLocator, FuncFormatter

from database_interface.manager import fetch_aliran_uang, fetch_riwayat_transaksi
from .utils.currency import indo

matplotlib.use("TkAgg")

class RiwayatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Riwayat Transaksi", font=("Arial", 20, "bold")).pack(pady=10)

        # Treeview untuk menampilkan tabel transaksi
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

        # Label total masuk dan keluat
        self.label_total_masuk = tk.Label(
            self, text="Total Uang Masuk: -", font=("Arial", 12)  
        )
        self.label_total_masuk.pack(pady=(5, 0))

        self.label_total_keluar = tk.Label(
            self, text="Total Uang Keluar: -",font=("Arial", 12)
        )
        self.label_total_keluar.pack(pady=(0, 10))


        # Tombol kembali
        ttk.Button(
            self,
            text="Kembali ke Dashboard",
            width=25,
            command=lambda: controller.show_frame("DashboardPage")
        ).pack(pady=10)

        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(fill='both', expand=True, padx=20, pady=10)

    def load_data(self):
        """Hitung ulang data transaksi setiap kali halaman dibuka."""
        rekening = self.controller.selected_rekening
        if rekening is None:
            messagebox.showerror("Error", "Rekening tidak ditemukan.")
            return

        nomor_rekening = rekening.nomor_rekening

        # Ambil riwayat transaksi
        try:
            riwayat = fetch_riwayat_transaksi(nomor_rekening)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil riwayat transaksi:\n{e}")
            return

        # Hapus isi tabel sebelumnya
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Masukkan data baru
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

        informasi_aliran = fetch_aliran_uang(rekening.nomor_rekening)

        # Fake data untuk nampilin fitur grafik
        informasi_aliran = {
            '2025-01': {'total_uang_masuk': 1500000, 'total_uang_keluar': 500000},
            '2025-02': {'total_uang_masuk': 1750000, 'total_uang_keluar': 600000},
            '2025-03': {'total_uang_masuk': 2000000, 'total_uang_keluar': 800000},
            '2025-04': {'total_uang_masuk': 2200000, 'total_uang_keluar': 900000},
            '2025-05': {'total_uang_masuk': 1800000, 'total_uang_keluar': 700000},
            '2025-06': {'total_uang_masuk': 2100000, 'total_uang_keluar': 950000},
            '2025-07': {'total_uang_masuk': 2300000, 'total_uang_keluar': 1000000},
            '2025-08': {'total_uang_masuk': 2500000, 'total_uang_keluar': 1100000},
            '2025-09': {'total_uang_masuk': 2700000, 'total_uang_keluar': 1200000},
            '2025-10': {'total_uang_masuk': 2600000, 'total_uang_keluar': 1150000},
            '2025-11': {'total_uang_masuk': 2800000, 'total_uang_keluar': 1300000},
            '2025-12': {'total_uang_masuk': 3000000, 'total_uang_keluar': 1500000},
            '2026-01': {'total_uang_masuk': 1500000, 'total_uang_keluar': 500000},
            '2026-02': {'total_uang_masuk': 1750000, 'total_uang_keluar': 600000},
            '2026-03': {'total_uang_masuk': 2000000, 'total_uang_keluar': 800000},
            '2026-04': {'total_uang_masuk': 2200000, 'total_uang_keluar': 900000},
            '2026-05': {'total_uang_masuk': 1800000, 'total_uang_keluar': 700000},
            '2026-06': {'total_uang_masuk': 2100000, 'total_uang_keluar': 950000},
            '2026-07': {'total_uang_masuk': 2300000, 'total_uang_keluar': 1000000},
            '2026-08': {'total_uang_masuk': 2500000, 'total_uang_keluar': 1100000},
            '2026-09': {'total_uang_masuk': 2700000, 'total_uang_keluar': 1200000},
            '2026-10': {'total_uang_masuk': 2600000, 'total_uang_keluar': 1150000},
            '2026-11': {'total_uang_masuk': 2800000, 'total_uang_keluar': 1300000},
            '2026-12': {'total_uang_masuk': 3000000, 'total_uang_keluar': 1500000},
            '2027-01': {'total_uang_masuk': 1500000, 'total_uang_keluar': 500000},
            '2027-02': {'total_uang_masuk': 1750000, 'total_uang_keluar': 600000},
            '2027-03': {'total_uang_masuk': 2000000, 'total_uang_keluar': 800000},
            '2027-04': {'total_uang_masuk': 2200000, 'total_uang_keluar': 900000},
            '2027-05': {'total_uang_masuk': 1800000, 'total_uang_keluar': 700000},
            '2027-06': {'total_uang_masuk': 2100000, 'total_uang_keluar': 950000},
            '2027-07': {'total_uang_masuk': 2300000, 'total_uang_keluar': 1000000},
            '2027-08': {'total_uang_masuk': 2500000, 'total_uang_keluar': 1100000},
            '2027-09': {'total_uang_masuk': 2700000, 'total_uang_keluar': 1200000},
            '2027-10': {'total_uang_masuk': 2600000, 'total_uang_keluar': 1150000},
            '2027-11': {'total_uang_masuk': 2800000, 'total_uang_keluar': 1300000},
            '2027-12': {'total_uang_masuk': 3000000, 'total_uang_keluar': 1500000},
            '2028-01': {'total_uang_masuk': 1500000, 'total_uang_keluar': 500000},
            '2028-02': {'total_uang_masuk': 1750000, 'total_uang_keluar': 600000},
            '2028-03': {'total_uang_masuk': 2000000, 'total_uang_keluar': 800000},
            '2028-04': {'total_uang_masuk': 2200000, 'total_uang_keluar': 900000},
            '2028-05': {'total_uang_masuk': 1800000, 'total_uang_keluar': 700000},
            '2028-06': {'total_uang_masuk': 2100000, 'total_uang_keluar': 950000},
            '2028-07': {'total_uang_masuk': 2300000, 'total_uang_keluar': 1000000},
            '2028-08': {'total_uang_masuk': 2500000, 'total_uang_keluar': 1100000},
            '2028-09': {'total_uang_masuk': 2700000, 'total_uang_keluar': 1200000},
            '2028-10': {'total_uang_masuk': 2600000, 'total_uang_keluar': 1150000},
            '2028-11': {'total_uang_masuk': 2800000, 'total_uang_keluar': 1300000},
            '2028-12': {'total_uang_masuk': 3000000, 'total_uang_keluar': 1500000},
        }

        total_masuk = 0
        total_keluar = 0


        for bulan, uang in informasi_aliran.items():
            total_masuk += uang['total_uang_masuk']
            total_keluar += uang['total_uang_keluar']

        self.label_total_masuk.config(text=f"Total income: {indo(total_masuk)}")
        self.label_total_keluar.config(text=f"Total expense: {indo(total_keluar)}")

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        months = sorted(informasi_aliran.keys())

        income = [informasi_aliran[month]['total_uang_masuk'] for month in months]
        expense = [informasi_aliran[month]['total_uang_keluar'] for month in months]

        figure = Figure(figsize=(14, 3), dpi=100)

        axis = figure.add_subplot(1, 1, 1)

        axis.plot(months, income, marker='o', label='Income', color='green')
        axis.plot(months, expense, marker='o', label='Expense', color='red')

        axis.set_title("Aliran Uang per Bulan")
        
        axis.set_xlabel("Bulan")
        axis.set_ylabel("Jumlah")

        axis.legend()
        axis.grid(True)

        axis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{int(x):,}"))
        axis.xaxis.set_major_locator(MaxNLocator(nbins=15)) # 15 x axis points look nice here

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
        toolbar.update()    
        toolbar.pack(fill='x')

        figure.autofmt_xdate()
