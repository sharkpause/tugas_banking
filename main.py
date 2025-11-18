import tkinter as tk

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title = 'Aplikasi'

        self.root.geometry('1000x700')

        self.root.mainloop()

app = MainApp(tk.Tk())