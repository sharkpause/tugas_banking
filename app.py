import tkinter as tk
from tkinter import messagebox
import hashlib
import random
from database_interface.database import db

def generate_no_rekening():
    # contoh: 10 digit angka acak
    return str(random.randint(1000000000, 9999999999))

def register_user():
    nama = entry_nama.get()
    email = entry_email.get()
    password = entry_password.get()
    no_hp = entry_no_hp.get()
    alamat = entry_alamat.get()

    if not all([nama, email, password, no_hp, alamat]):
        messagebox.showwarning("Peringatan", "Semua kolom wajib diisi!")
        return

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = db
        cursor = conn.cursor()

        # 1️⃣ Simpan data nasabah
        cursor.execute("""
            INSERT INTO nasabah (nama, password_hash, email, no_hp, alamat)
            VALUES (%s, %s, %s, %s, %s)
        """, (nama, password_hash, email, no_hp, alamat))
        conn.commit()

        # Ambil ID nasabah yang baru saja ditambahkan
        id_nasabah = cursor.lastrowid

        # 2️⃣ Buat rekening otomatis untuk nasabah baru
        no_rekening = generate_no_rekening()
        cursor.execute("""
            INSERT INTO rekening (id_nasabah, no_rekening, saldo)
            VALUES (%s, %s, %s)
        """, (id_nasabah, no_rekening, 0.00))
        conn.commit()

        messagebox.showinfo("Sukses", f"Registrasi berhasil!\nNo Rekening: {no_rekening}")

        # Kosongkan form
        entry_nama.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_no_hp.delete(0, tk.END)
        entry_alamat.delete(0, tk.END)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Gagal registrasi: {err}")
    finally:
        cursor.close()
        conn.close()

# --- GUI Register ---
window = tk.Tk()
window.title("Registrasi Nasabah - M Banking")
window.geometry("400x350")
window.resizable(False, False)

tk.Label(window, text="REGISTRASI NASABAH", font=("Arial", 14, "bold")).pack(pady=10)

frame = tk.Frame(window)
frame.pack()

tk.Label(frame, text="Nama:").grid(row=0, column=0, sticky="e")
entry_nama = tk.Entry(frame, width=30)
entry_nama.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Email:").grid(row=1, column=0, sticky="e")
entry_email = tk.Entry(frame, width=30)
entry_email.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Password:").grid(row=2, column=0, sticky="e")
entry_password = tk.Entry(frame, show="*", width=30)
entry_password.grid(row=2, column=1, pady=5)

tk.Label(frame, text="No HP:").grid(row=3, column=0, sticky="e")
entry_no_hp = tk.Entry(frame, width=30)
entry_no_hp.grid(row=3, column=1, pady=5)

tk.Label(frame, text="Alamat:").grid(row=4, column=0, sticky="e")
entry_alamat = tk.Entry(frame, width=30)
entry_alamat.grid(row=4, column=1, pady=5)

tk.Button(window, text="Daftar", width=20, bg="green", fg="white", command=register_user).pack(pady=10)

window.mainloop()
