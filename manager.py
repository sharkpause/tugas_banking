from __future__ import annotations

# Script untuk manage class dan operasi database (abstraction) belum selesai

from nasabah import Nasabah
from rekening import Rekening, nomor_rekening_ke_Rekening
from riwayat_transaksi import RiwayatTransaksi as RT, new_RT

from database import Database
from CustomClasses import JenisTransaksi, Status, TransactionError

db = Database()

def transaksi(
    jenis: JenisTransaksi,
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening_sumber: Rekening,
    Rekening_tujuan: Rekening = None
) -> Status.SUCCESS | Status.ERROR:
    """
    
    Pembuatan riwayat transaksi sudah ditangani function ini.
    JANGAN PERNAH CALL FUNCTION increase_balance DAN decrease_balance ATAU
    MEMBUAT RiwayatTransaki SENDIRI SEMUANYA HARUS LEWAT FUNCTION INI

    jenis: JenisTransaksi.DEPOSIT atau JenisTransaksi.WITHDRAW atau JenisTransaksi.TRANSFER (terdapat dalam CustomClasses.py)
    jumlah_uang: integer
    datetime_transaksi format:      YYYY-mm-dd HH:mm:ss
                       penjelasan:  Tahun-bulan-hari Jam:menit:detik
                       contoh:      2025-11-14 20:10:44
    Rekening_sumber: Objek Rekening
    Rekening_tujuan: Objek Rekening
    KOSONGKAN "Rekening_tujuan" dalam DEPOSIT dan WITHDRAW, ITU HANYA UNTUK TRANSFER
    
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
        case _:
            return Status.ERROR

def buat_nasabah_baru(nama: str, password: str, email: str, nomor_telepon: str, alamat: str) -> Nasabah:
    """

    SELALU GUNAKAN FUNCTION INI UNTUK MEMBUAT NASABAH BARU YANG INGIN DISIMPAN DALAM DATABASE

    nama: Nama lengkap nasabah
    password: Password "plain-text" JANGAN DI-HASH, SUDAH DI-HASH DALAM CONSTRUCTOR NASABAH
    email: Email nasabah
    nomor_telepon: Nomor telepon nasabah
    alamat: Alamat lengkap nasabah

    """
    n = Nasabah(nama, password, email, nomor_telepon, alamat)
    n._Nasabah__create_in_database()
    n._Nasabah__create_new_rekening()

    return n

# Testing

# r = nomor_rekening_ke_Rekening('34674875834793492200')
# transaksi(JenisTransaksi.DEPOSIT, 20_000, '2025-11-04 20:29:10', r)
# print('Saldo rekening baru setelah deposit:', r.saldo)

# don = buat_nasabah_baru('Don', 'password', 'shark@finfeed.com', '081231231111', 'Jl. Asia')
# transaksi(JenisTransaksi.DEPOSIT, 30_000, '2025-11-04 20:29:10', don.rekening)

# rachel = buat_nasabah_baru('Rachel', 'password', 'beargirl@finfeed.com', '0813332134145', 'Jl. Asia')
# transaksi(JenisTransaksi.DEPOSIT, 20_000, '2025-11-04 20:29:10', rachel.rekening)

# transaksi(JenisTransaksi.TRANSFER, 15_000, '2025-11-04 20:29:10', don.rekening, rachel.rekening)