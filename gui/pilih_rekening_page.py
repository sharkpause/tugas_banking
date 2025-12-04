import tkinter as tk
from tkinter import ttk

class PilihRekeningPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="Pilih Rekening", font=("Arial", 16))
        title.pack(pady=10)

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=10)

    def load_data(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        user = self.controller.current_user
        rekenings = getattr(user, "rekening", [])

        for r in rekenings:
            btn = ttk.Button(
                self.buttons_frame, 
                text=f"{r.nomor_rekening}: {r.jenis_rekening}",
                command=lambda r=r: self.select_rekening(r)
            )
            btn.pack(pady=5)

    def select_rekening(self, rekening):
        print(f"Selected rekening: {rekening.nomor_rekening}")
        self.controller.selected_rekening = rekening

