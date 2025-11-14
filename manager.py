from __future__ import annotations

# Script untuk manage class dan operasi database (abstraction) belum selesai

from nasabah import Nasabah
from rekening import Rekening
from riwayat_transaksi import RiwayatTransaksi as RT

from database import Database
from CustomClasses import JenisTransaksi, Status, TransactionError
from utilitas import nomor_rekening_ke_Rekening

db = Database()

def new_RT(nomor_rekening_sumber: str, nomor_rekening_tujuan: str, jenis: JenisTransaksi, jumlah_uang: int, datetime_transaksi: str) -> RT:
    rt = RT(nomor_rekening_sumber, nomor_rekening_tujuan, JenisTransaksi.DEPOSIT, jumlah_uang, datetime_transaksi)
    rt._RiwayatTransaksi__create_in_database()

def transaksi(
    jenis: JenisTransaksi,
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening_sumber: Rekening,
    Rekening_tujuan: Rekening = None
) -> Status.SUCCESS:
    """
    Untuk deposit dan withdrawal, kosongkan "nomor_rekening_tujuan", itu hanya untuk transfer
    """
    
    match jenis:
        case JenisTransaksi.DEPOSIT:
            Rekening_sumber._Rekening__increase_balance(jumlah_uang)

            new_RT(Rekening_sumber.nomor_rekening, None, JenisTransaksi.DEPOSIT, jumlah_uang, datetime_transaksi)
            return Status.SUCCESS
        case JenisTransaksi.WITHDRAW:
            Rekening_sumber._Rekening__decrease_balance(jumlah_uang)

            new_RT(Rekening_sumber.nomor_rekening, None, JenisTransaksi.DEPOSIT, jumlah_uang, datetime_transaksi)
            return Status.SUCCESS
        case JenisTransaksi.TRANSFER:
            if not Rekening_tujuan:
                raise TransactionError({
                    'status': Status.ERROR,
                    'type': ErrorType.MISSING_ARGUMENT,
                    'message': 'Rekening tujuan tidak bisa kosong'
                })

            new_RT(Rekening_sumber.nomor_rekening, Rekening_tujuan.nomor_rekening, JenisTransaksi.DEPOSIT, jumlah_uang, datetime_transaksi)
            Rekening_sumber._Rekening__decrease_balance(jumlah_uang)
            Rekening_tujuan._Rekening__increase_balance(jumlah_uang)

            return Status.SUCCESS

def buat_nasabah_baru(nama: str, password: str, email: str, nomor_telepon: str, alamat: str) -> Nasabah:
    n = Nasabah(nama, password, email, nomor_telepon, alamat)
    n._Nasabah__create_in_database()
    n._Nasabah__create_new_rekening()

    return n

# Testing

# r = nomor_rekening_ke_Rekening('34674875834793492200')
# transaksi(JenisTransaksi.DEPOSIT, 20_000, '2025-11-04 20:29:10', r)
# print('Saldo rekening baru setelah deposit:', r.saldo)

don = buat_nasabah_baru('Don', 'password', 'shark@finfeed.com', '081231231111', 'Jl. Asia')
transaksi(JenisTransaksi.DEPOSIT, 30_000, '2025-11-04 20:29:10', don.rekening)

rachel = buat_nasabah_baru('Rachel', 'password', 'beargirl@finfeed.com', '0813332134145', 'Jl. Asia')
transaksi(JenisTransaksi.DEPOSIT, 20_000, '2025-11-04 20:29:10', rachel.rekening)

transaksi(JenisTransaksi.TRANSFER, 15_000, '2025-11-04 20:29:10', don.rekening, rachel.rekening)