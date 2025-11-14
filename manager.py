from __future__ import annotations

# Script untuk manage class dan operasi database (abstraction) belum selesai

from nasabah import Nasabah
from rekening import Rekening
from riwayat_transaksi import RiwayatTransaksi as RT

from database import Database
from CustomClasses import JenisTransaksi, Status
from utilitas import nomor_rekening_ke_Rekening

db = Database()

def transaksi(
    jenis: JenisTransaksi,
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening_sumber: Rekening,
    Rekening_tujuan: Rekening = None
) -> Status.SUCCESS | Status.ERROR:
    """
    Untuk deposit dan withdrawal, kosongkan "nomor_rekening_tujuan", itu hanya untuk transfer
    """
    
    match jenis:
        case JenisTransaksi.DEPOSIT:
            Rekening_sumber.tambah_saldo(jumlah_uang)

            return Status.SUCCESS
        case JenisTransaksi.WITHDRAW:
            Rekening_sumber.kurang_saldo(jumlah_uang)

            return Status.SUCCESS

def buat_nasabah_baru(nama: str, password: str, email: str, nomor_telepon: str, alamat: str) -> Nasabah:
    n = Nasabah(nama, password, email, nomor_telepon, alamat)
    n._Nasabah__create_in_database()
    n._Nasabah__buat_rekening_baru()

    return n

# # Testing
# n = Nasabah('Don', '123', '123@123.com', '081231231111', 'aj')
# n.rekening.tambah_saldo(1_000)
# print('Saldo rekening Don:', n.rekening.saldo)

# r = nomor_rekening_ke_Rekening('34674875834793492200')
# transaksi(JenisTransaksi.DEPOSIT, 20_000, '2025-11-04 20:29:10', r)
# print('Saldo rekening baru setelah deposit:', r.saldo)

n = buat_nasabah_baru('Rachel', 'password', 'beargirl@finfeed.com', '0813332134145', 'Jl. Asia')
print(n.nama)
transaksi(JenisTransaksi.WITHDRAW, 20000, '2025-11-04 20:29:10', n.rekening)