import tkinter as tk

from gui.login_page import LoginPage
from gui.pilih_rekening_page import PilihRekeningPage
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

        self.current_user = None
        self.current_rekening = None

        container = tk.Frame(self)
        container.pack(expand=True)

        self.frames = {}

        pages = {
            "LoginPage": LoginPage,
            "RegisterPage": RegisterPage,
            "DashboardPage": DashboardPage,
            "TransferPage": TransferPage,
            "TransaksiPage": TransaksiPage,        
            "RiwayatPage": RiwayatPage,
            "AdminPage": AdminPage,
            "PilihRekeningPage": PilihRekeningPage
        }

        for page_name, PageClass in pages.items():
            frame = PageClass(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        if hasattr(frame, "load_data"):
            frame.load_data()

        frame.tkraise()
