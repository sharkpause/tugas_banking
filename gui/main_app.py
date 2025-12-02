import tkinter as tk

# Import semua halaman GUI
from gui.login_page import LoginPage
from gui.register_page import RegisterPage
from gui.dashboard_page import DashboardPage
from gui.transfer_page import TransferPage
from gui.transaksi_page import TransaksiPage
from gui.riwayat_page import RiwayatPage
from gui.admin_page import AdminPage

from ttkbootstrap import Style
from ttkbootstrap.constants import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tugas Banking - ATM App")
        self.geometry("800x500")

        self.style = Style(theme='superhero')

        # Variable global untuk user yang sedang login
        self.current_user = None
        self.current_rekening = None

        container = tk.Frame(self)
        container.pack(expand=True)

        self.frames = {}

        # Daftar semua halaman GUI
        pages = {
            "LoginPage": LoginPage,
            "RegisterPage": RegisterPage,
            "DashboardPage": DashboardPage,
            "TransferPage": TransferPage,
            "TransaksiPage": TransaksiPage,        # Deposit / Withdraw
            "RiwayatPage": RiwayatPage,
            "AdminPage": AdminPage
        }

        # Generate frame
        for page_name, PageClass in pages.items():
            frame = PageClass(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Tampilkan halaman login pertama kali
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        # Jika halaman punya fungsi refresh/load_data, panggil otomatis
        if hasattr(frame, "load_data"):
            frame.load_data()

        frame.tkraise()
