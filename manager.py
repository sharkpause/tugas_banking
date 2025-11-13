# Script untuk manage class dan operasi database (abstraction) belum selesai

from typing import Literal

from nasabah import Nasabah
from rekening import Rekening
from riwayat_transaksi import RiwayatTransaksi as RT

class Transaksi:
    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3

def nasabah_baru(nama: str, password: str, email: str, nomor_telepon: str, alamat: str):
    nasabah = Nasabah(nama, password, email, nomor_telepon, alamat)

    return nasabah

# def transaksi(
#     jenis: Literal[Transaksi.DEPOSIT, Transaksi.WITHDRAW, Transaksi.TRANSFER],
#     jumlah_uang: int,
#     datetime_transaksi: str,
#     nomor_rekening_sumber: str,
#     nomor_rekening_tujuan: str = None
# ):
#     if jenis == Transaksi.DEPOSIT:
#         pass



# Testing
n = nasabah_baru('Don', '123', '123@123.com', '081231231111', 'aj')
n.rekening.tambah_saldo(1000)
print(n.rekening.saldo)