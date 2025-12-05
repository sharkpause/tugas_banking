from datetime import datetime

import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.ticker import MaxNLocator, FuncFormatter

from tkinter import messagebox, simpledialog
from database_interface.manager import login_admin, fetch_semua_user, deposit, withdraw, transfer, fetch_riwayat_transaksi, tutup_rekening, buka_rekening, fetch_aliran_uang
from .utils.currency import indo

class AdminLoginFrame (tk.Frame) :
    def __init__ (self, master, on_success, controller) :
        super ().__init__(master)

        self.on_success = on_success
        self.controller = controller

        self._build()

    def _build (self):
        lbl = tk.Label(self, text= "Admin Mode - Login", font=('Segoe UI', 14, 'bold'))
        lbl.pack(pady=8)

        frm = tk.Frame (self)
        frm.pack (pady=4)

        tk.Label(frm, text="Admin Token:").grid(row=0, column=0, sticky='e')
        self.token_var = tk.StringVar()
        tk.Entry(frm, textvariable=self.token_var, width=40, show='*').grid(row=0, column=1, padx=6)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Login", command=self._try_login).pack(side='left', padx=6)
        tk.Button(btn_frame, text="Back", command=lambda: self.controller.show_frame('LoginPage')).pack(side='left', padx=6)

    def _try_login(self):
        token = self.token_var.get().strip()
        if not token:
            messagebox.showwarning("Token kosong", "Masukkan token admin terlebih dahulu")
            return
        try:
            res = login_admin(token)
            if res == 0:
                self.on_success()
            else:
                messagebox.showerror("Login gagal", f"Respon tidak dikenal: {res}")
        except Exception as e:
            try:
                msg = e.args[0]
            except Exception:
                msg = str(e)
            messagebox.showerror("Login error", f"Login admin gagal: {msg}")


class AdminDashboardFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.users = [] 
        self.rekening_map = {}  
        self._build()
        self._refresh_users()

    def _build(self):
        hdr = tk.Frame(self)
        hdr.pack(fill='x', pady=6)
        tk.Label(hdr, text="Admin Dashboard", font=(None, 14, 'bold')).pack(side='left', padx=6)
        tk.Button(hdr, text="Refresh", command=self._refresh_users).pack(side='right', padx=6)
        tk.Button(hdr, text="Logout", command=lambda: self.master.controller.show_frame('LoginPage')).pack(side='right')

        body = tk.PanedWindow(self, orient='horizontal')
        body.pack(fill='both', expand=True, padx=6, pady=6)

        left = tk.Frame(body)
        body.add(left, width=420)
        self.tree = ttk.Treeview(left, columns=("email", "telepon"), show='headings', selectmode='browse')
        self.tree.heading('email', text='Email')
        self.tree.heading('telepon', text='Telepon')
        self.tree.pack(fill='both', expand=True, side='top')
        self.tree.bind('<<TreeviewSelect>>', self._on_user_select)

        right = tk.Frame(body)
        body.add(right)

        self.detail_lbl = tk.Label(right, text="Pilih user untuk lihat detail", justify='left')
        self.detail_lbl.pack(anchor='nw')

        tk.Label(right, text="Rekening:").pack(anchor='nw', pady=(8,0))
        self.acc_listbox = tk.Listbox(right, height=6)
        self.acc_listbox.pack(fill='x')

        action_fr = tk.Frame(right)
        action_fr.pack(fill='x', pady=8)
        tk.Button(action_fr, text="Deposit", command=self._action_deposit).pack(side='left', padx=4)
        tk.Button(action_fr, text="Withdraw", command=self._action_withdraw).pack(side='left', padx=4)
        tk.Button(action_fr, text="Transfer", command=self._action_transfer).pack(side='left', padx=4)
        tk.Button(action_fr, text="Riwayat Transaksi", command=self._action_riwayat).pack(side='left', padx=4)
        tk.Button(action_fr, text="Tutup rekening", command=self._action_tutup).pack(side='left', padx=4)
        tk.Button(action_fr, text="Buka rekening", command=self._action_buka).pack(side='left', padx=4)

        self.status_var = tk.StringVar(value='Siap')
        tk.Label(self, textvariable=self.status_var, anchor='w').pack(fill='x', padx=6, pady=(0,6))

    def _action_tutup(self):
        try:
            nomor_rekening = self._get_selected_rekening().nomor_rekening
            tutup_rekening(nomor_rekening)
        except Exception as e:
            print(e)
            messagebox.showerror("Admin Error", "Terjadi kesalahan tolong coba lagi!")

    def _action_buka(self):
        try:
            nomor_rekening = self._get_selected_rekening().nomor_rekening
            buka_rekening(nomor_rekening)
        except Exception as e:
            print(e)
            messagebox.showerror("Admin Error", "Terjadi kesalahan tolong coba lagi!")

    def _set_status(self, text):
        self.status_var.set(text)

    def _refresh_users(self):
        self._set_status('Mengambil daftar nasabah...')
        try:
            self.users = fetch_semua_user()
        except Exception as e:
            messagebox.showerror("Fetch error", f"Gagal mengambil data nasabah: {e}")
            self._set_status('Error')
            return

        for i in self.tree.get_children():
            self.tree.delete(i)
        self.rekening_map.clear()
        for nasabah in self.users:
            try:
                email = getattr(nasabah, 'email', '-')
                telepon = getattr(nasabah, 'nomor_telepon', '-')
                display = getattr(nasabah, 'nama', '<tanpa nama>')
                uid = str(nasabah.nomor_telepon) if hasattr(nasabah, 'nomor_telepon') else str(id(nasabah))
                
                self.tree.insert('', 'end', iid=uid, values=(email, telepon), text=display)
                
                if hasattr(nasabah, 'rekening') and nasabah.rekening:
                    for r in nasabah.rekening:
                        no = getattr(r, 'nomor_rekening', None)
                        if no:
                            self.rekening_map[no] = r
            except Exception as e:
                print(f"Error processing nasabah {getattr(nasabah, 'nomor_telepon', '<unknown>')}: {e}")
                continue
    
        self._set_status(f'Ditemukan {len(self.users)} nasabah')

    def _on_user_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        uid = sel[0]
        nas = None
        for n in self.users:
            if str(n.nomor_telepon) == uid:
                nas = n
                break
        if nas is None:
            return

        lines = []
        lines.append(f"Nama: {getattr(nas, 'nama', '-')}")
        lines.append(f"Email: {getattr(nas, 'email', '-')}")
        lines.append(f"Telepon: {getattr(nas, 'nomor_telepon', '-')}")
        lines.append(f"Alamat: {getattr(nas, 'alamat', '-')}")
        self.detail_lbl.config(text='\n'.join(lines))

        self.acc_listbox.delete(0, 'end')
        if hasattr(nas, 'rekening') and nas.rekening:
            for r in nas.rekening:
                no = getattr(r, 'nomor_rekening', '<no>')
                saldo = getattr(r, 'jumlah_saldo', 0)
                jenis = getattr(r, 'jenis_rekening', 'checking')
                status = getattr(r, 'status_buka', 'unknown')

                if status == True:
                    status = 'buka'
                elif status == False:
                    status = 'tutup'

                self.acc_listbox.insert('end', f"{no} | {status} | {jenis} | Saldo: {saldo}")

    def _get_selected_rekening(self):
        sel_idx = self.acc_listbox.curselection()
        if not sel_idx:
            messagebox.showwarning("Pilih rekening", "Pilih rekening terlebih dahulu pada daftar rekening.")
            return None
        text = self.acc_listbox.get(sel_idx)
        no = text.split(' | ')[0]
        return self.rekening_map.get(no)

    def _action_deposit(self):
        rek = self._get_selected_rekening()
        if not rek:
            return
        amt = simpledialog.askinteger("Deposit", "Masukkan jumlah (integer):", minvalue=1)
        if not amt:
            return
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            tid = deposit(amt, dt, rek)
            messagebox.showinfo("Sukses", f"Deposit berhasil. ID transaksi: {tid}")
            self._refresh_users()
        except Exception as e:
            messagebox.showerror("Error", f"Deposit gagal: {e}")

    def _action_withdraw(self):
        rek = self._get_selected_rekening()
        if not rek:
            return
        amt = simpledialog.askinteger("Withdraw", "Masukkan jumlah (integer):", minvalue=1)
        if not amt:
            return
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            res = withdraw(amt, dt, rek)
            if isinstance(res, int):
                messagebox.showinfo("Sukses", f"Withdraw berhasil. ID: {res}")
            else:
                messagebox.showinfo("Result", f"Hasil: {res}")
            self._refresh_users()
        except Exception as e:
            messagebox.showerror("Error", f"Withdraw gagal: {e}")

    def _action_transfer(self):
        src = self._get_selected_rekening()
        if not src:
            return

        choices = list(self.rekening_map.keys())
        if not choices:
            messagebox.showwarning("Tidak ada rekening target", "Tidak ada rekening tersedia sebagai target.")
            return
        target_no = simpledialog.askstring("Transfer", f"Masukkan nomor rekening tujuan. Contoh:\nAvailable:\n{', '.join(choices)}")
        if not target_no:
            return
        target_no = target_no.strip()
        tgt = self.rekening_map.get(target_no)
        if not tgt:
            messagebox.showerror("Rekening tidak ditemukan", "Nomor rekening tujuan tidak ditemukan. Gunakan daftar rekening yang tersedia.")
            return
        amt = simpledialog.askinteger("Transfer", "Masukkan jumlah transfer (integer):", minvalue=1)
        if not amt:
            return
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            tid = transfer(amt, dt, src, tgt)
            messagebox.showinfo("Sukses", f"Transfer berhasil. ID transaksi: {tid}")
            self._refresh_users()
        except Exception as e:
            messagebox.showerror("Error", f"Transfer gagal: {e}")

    def _action_riwayat(self):
        rek = self._get_selected_rekening()
        if not rek:
            return
        no = getattr(rek, 'nomor_rekening', None)
        if not no:
            messagebox.showerror("Error", "Nomor rekening tidak valid.")
            return

        try:
            rows = fetch_riwayat_transaksi(no)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil riwayat: {e}")
            return

        try:
            informasi_aliran = fetch_aliran_uang(no)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil aliran uang: {e}")
            informasi_aliran = {}

        win = tk.Toplevel(self)
        win.title(f"Riwayat & Grafik - {no}")

        txt = tk.Text(win, width=80, height=20)
        txt.pack(fill='both', expand=True)
        if not rows:
            txt.insert('end', 'Tidak ada riwayat.\n')
        else:
            for r in rows:
                try:
                    t = getattr(r, 'datetime_transaksi', getattr(r, 'datetime', ''))
                    jenis = getattr(r, 'jenis_transaksi', getattr(r, 'jenis', ''))
                    amt = getattr(r, 'jumlah_uang', getattr(r, 'amount', ''))
                    src = getattr(r, 'nomor_rekening_sumber', getattr(r, 'sumber', ''))
                    dst = getattr(r, 'nomor_rekening_tujuan', getattr(r, 'tujuan', ''))
                    line = f"{t} | {jenis} | {amt} | {src} -> {dst}\n"
                except Exception:
                    line = repr(r) + "\n"
                txt.insert('end', line)

        total_masuk = sum(u['total_uang_masuk'] for u in informasi_aliran.values())
        total_keluar = sum(u['total_uang_keluar'] for u in informasi_aliran.values())

        label_total_masuk = tk.Label(win, text=f"Total income: {indo(total_masuk)}")
        label_total_masuk.pack()
        label_total_keluar = tk.Label(win, text=f"Total expense: {indo(total_keluar)}")
        label_total_keluar.pack()

        if informasi_aliran:
            graph_frame = tk.Frame(win)
            graph_frame.pack(fill='both', expand=True)

            months = sorted(informasi_aliran.keys())
            income = [informasi_aliran[m]['total_uang_masuk'] for m in months]
            expense = [informasi_aliran[m]['total_uang_keluar'] for m in months]

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
            figure.autofmt_xdate()

            canvas = FigureCanvasTkAgg(figure, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

            toolbar = NavigationToolbar2Tk(canvas, graph_frame)
            toolbar.update()
            toolbar.pack(fill='x')

class AdminPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.frame = ttk.Frame(self)

        self.frame.pack(fill='both', expand=True)
        self.login_frame = AdminLoginFrame(self, on_success=self._show_dashboard, controller=controller)
        self.dashboard = AdminDashboardFrame(self)
        self.login_frame.pack(fill='both', expand=True)

    def _show_dashboard(self):
        self.login_frame.pack_forget()
        self.dashboard.pack(fill='both', expand=True)

    def show_login(self):
        self.dashboard.pack_forget()
        self.login_frame.pack(fill='both', expand=True)

    def show_main(self):
        self.controller.show_frame('LoginPage')

