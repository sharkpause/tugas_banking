from __future__ import annotations

from nasabah import Nasabah
from rekening import Rekening
from riwayat_transaksi import RiwayatTransaksi as RT, new_RT

from database import db
from CustomClasses import JenisTransaksi, Status, TransactionError, DatabaseError

def deposit(
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening
) -> Status.SUCECSS | Status.ERROR:
    """
    
    Pembuatan riwayat transaksi sudah ditangani function ini.
    JANGAN PERNAH CALL FUNCTION increase_balance DAN decrease_balance ATAU
    MEMBUAT RiwayatTransaki SENDIRI SEMUANYA HARUS LEWAT FUNCTION INI

    jumlah_uang: integer
    datetime_transaksi format:      YYYY-mm-dd HH:mm:ss
                       penjelasan:  Tahun-bulan-hari Jam:menit:detik
                       contoh:      2025-11-14 20:10:44
    Rekening: Objek Rekening

    """

    try:
        balance_status = Rekening._Rekening__increase_balance(jumlah_uang)
        new_RT(Rekening.nomor_rekening, None, JenisTransaksi.DEPOSIT, jumlah_uang, datetime_transaksi)
        
        db.commit()

        return Status.SUCCESS
    except:
        db.rollback()
        raise

def withdraw(
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening
) -> Status.SUCCESS | Status.ERROR:
    """
    
    Pembuatan riwayat transaksi sudah ditangani function ini.
    JANGAN PERNAH CALL FUNCTION increase_balance DAN decrease_balance ATAU
    MEMBUAT RiwayatTransaki SENDIRI SEMUANYA HARUS LEWAT FUNCTION INI

    jumlah_uang: integer
    datetime_transaksi format:      YYYY-mm-dd HH:mm:ss
                       penjelasan:  Tahun-bulan-hari Jam:menit:detik
                       contoh:      2025-11-14 20:10:44
    Rekening: Objek Rekening

    """

    try:
        Rekening._Rekening__decrease_balance(jumlah_uang)
        new_RT(Rekening.nomor_rekening, None, JenisTransaksi.DEPOSIT, jumlah_uang, datetime_transaksi)
        
        db.commit()
        
        return Status.SUCCESS
    except:
        db.rollback()
        raise

def transfer(
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening_sumber: Rekening,
    Rekening_tujuan: Rekening
) -> Status.SUCCESS | Status.ERROR:
    """
    
    Pembuatan riwayat transaksi sudah ditangani function ini.
    JANGAN PERNAH CALL FUNCTION increase_balance DAN decrease_balance ATAU
    MEMBUAT RiwayatTransaki SENDIRI SEMUANYA HARUS LEWAT FUNCTION INI

    jumlah_uang: integer
    datetime_transaksi format:      YYYY-mm-dd HH:mm:ss
                       penjelasan:  Tahun-bulan-hari Jam:menit:detik
                       contoh:      2025-11-14 20:10:44
    Rekening_sumber: Objek Rekening
    Rekening_tujuan: Objek Rekening
    
    """

    try:
        Rekening_sumber._Rekening__decrease_balance(jumlah_uang)
        Rekening_tujuan._Rekening__increase_balance(jumlah_uang)

        new_RT(Rekening_sumber.nomor_rekening, Rekening_tujuan.nomor_rekening, JenisTransaksi.TRANSFER, jumlah_uang, datetime_transaksi)

        db.commit()

        return Status.SUCCESS
    except:
        db.rollback()
        raise

def buat_nasabah_baru(nama: str, password: str, email: str, nomor_telepon: str, alamat: str) -> Nasabah:
    """

    SELALU GUNAKAN FUNCTION INI UNTUK MEMBUAT NASABAH BARU YANG INGIN DISIMPAN DALAM DATABASE

    nama: Nama lengkap nasabah
    password: Password "plain-text" JANGAN DI-HASH, SUDAH DI-HASH DALAM CONSTRUCTOR NASABAH
    email: Email nasabah
    nomor_telepon: Nomor telepon nasabah
    alamat: Alamat lengkap nasabah

    """

    try:
        n = Nasabah(nama, password, email, nomor_telepon, alamat)
        n._Nasabah__create_in_database()
        n._Nasabah__create_new_rekening()

        db.commit()

        return n
    except:
        db.rollback()
        raise

def hapus_nasabah(nomor_telepon: str = None, email: str = None):
    try:
        if nomor_telepon:
            query: str = 'DELETE FROM nasabah WHERE nomor_telepon = %s'
            val: tuple = (nomor_telepon,)

            db.exec_query(query, val)
            db.commit()
        elif email:
            query: str = 'DELETE FROM nasabah WHERE email = %s'
            val: tuple = (email,)

            db.exec_query(query, val)
            db.commit()
    except:
        db.rollback()
        raise