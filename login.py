import tkinter as tk
from tkinter import messagebox
import hashlib

from database_interface.database import db
from database_interface.manager import login_nasabah

def login_user():
    email = entry_email.get()
    password = entry_password.get()

    if not email or not password:
        messagebox.showwarning("Peringatan", "Nomor telepon dan password wajib diisi!")
        return

    try:
        # Assuming nomor_telepon is equivalent to email here, adjust if needed
        result = login_nasabah(email, password)
        user = result['object']

        messagebox.showinfo("Sukses", f"Selamat datang, {user.nama}!")
        open_dashboard(user)
    except Exception as e:
        print('Error:', e)
        # You can customize the error message if login_nasabah raises a specific exception
        messagebox.showerror("Gagal", "Email atau password salah!")

def open_dashboard(user):
    dashboard = tk.Toplevel(window)
    dashboard.title("Dashboard Nasabah")
    dashboard.geometry("400x300")

    # Ambil data rekening nasabah
    conn = db
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT no_rekening, saldo FROM rekening WHERE id_nasabah = %s", (user['id'],))
    rekening = cursor.fetchone()
    cursor.close()
    conn.close()

    tk.Label(dashboard, text=f"Selamat datang, {user['nama']}", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(dashboard, text=f"Email: {user['email']}").pack(pady=2)
    tk.Label(dashboard, text=f"No HP: {user['no_hp']}").pack(pady=2)
    tk.Label(dashboard, text=f"Alamat: {user['alamat']}").pack(pady=5)
    tk.Label(dashboard, text=f"No Rekening: {rekening['no_rekening']}").pack(pady=2)
    tk.Label(dashboard, text=f"Saldo: Rp {rekening['saldo']:.2f}").pack(pady=5)

    tk.Button(dashboard, text="Keluar", command=dashboard.destroy).pack(pady=10)

# --- GUI Login ---
window = tk.Tk()
window.title("Login Nasabah - M Banking")
window.geometry("350x250")
window.resizable(False, False)

tk.Label(window, text="LOGIN NASABAH", font=("Arial", 14, "bold")).pack(pady=10)

frame = tk.Frame(window)
frame.pack()

tk.Label(frame, text="Email:").grid(row=0, column=0, sticky="e")
entry_email = tk.Entry(frame, width=30)
entry_email.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e")
entry_password = tk.Entry(frame, show="*", width=30)
entry_password.grid(row=1, column=1, pady=5)

tk.Button(window, text="Login", width=15, bg="blue", fg="white", command=login_user).pack(pady=10)

window.mainloop()

