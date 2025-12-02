from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from database_interface.CustomClasses import CredentialsError

try:
    from nasabah import Nasabah
    from rekening import Rekening
    from riwayat_transaksi import new_RT
    from database import db
    from CustomClasses import JenisTransaksi, Status, StringJenisTransaksi, ErrorType
    from riwayat_transaksi import RiwayatTransaksi

    from helper import nomor_telepon_ke_Nasabah, nomor_telepon_ke_Rekening
except:
    from .nasabah import Nasabah
    from .rekening import Rekening
    from .riwayat_transaksi import new_RT
    from .database import db
    from .CustomClasses import JenisTransaksi, Status, StringJenisTransaksi, ErrorType
    from .riwayat_transaksi import RiwayatTransaksi

    from .helper import nomor_telepon_ke_Nasabah, nomor_telepon_ke_Rekening

def deposit(
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening
) -> int:
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
        id = new_RT(Rekening.nomor_rekening, None, JenisTransaksi.DEPOSIT, jumlah_uang, datetime_transaksi)
        
        db.commit()

        return id
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

    Return RiwayatTransaksi ID

    """

    try:
        Rekening._Rekening__decrease_balance(jumlah_uang)
        id = new_RT(Rekening.nomor_rekening, None, JenisTransaksi.WITHDRAW, jumlah_uang, datetime_transaksi)
        
        db.commit()
        
        return id
    except:
        db.rollback()
        raise

def transfer(
    jumlah_uang: int,
    datetime_transaksi: str,
    Rekening_sumber: Rekening,
    Rekening_tujuan: Rekening
) -> int:
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

    Return RiwayatTransaksi ID
    
    """

    try:
        Rekening_sumber._Rekening__decrease_balance(jumlah_uang)
        Rekening_tujuan._Rekening__increase_balance(jumlah_uang)

        id = new_RT(Rekening_sumber.nomor_rekening, Rekening_tujuan.nomor_rekening, JenisTransaksi.TRANSFER, jumlah_uang, datetime_transaksi)

        db.commit()

        return id
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

def tutup_nasabah(nomor_telepon: str | None = None, email: str | None = None):
    try:
        if nomor_telepon:
            query: str = 'UPDATE nasabah SET status_buka = false WHERE nomor_telepon = %s'
            val: tuple = (nomor_telepon,)

            db.exec_query(query, val)
            db.commit()
        elif email:
            query: str = 'UPDATE nasabah SET status_buka = false WHERE email = %s'
            val: tuple = (email,)

            db.exec_query(query, val)
            db.commit()
    except:
        db.rollback()
        raise

def login_nasabah(nomor_telepon: str, password: str):
    '''

    Function ini melogin nasabah menggunakan database operasi
    Jangan meng-call function login dalam objek Nasabah secara langsung

    '''
    try:
        nasabah = nomor_telepon_ke_Nasabah(nomor_telepon)
        result = nasabah._Nasabah__login(password)

        nasabah.rekening = nomor_telepon_ke_Rekening(nasabah.nomor_telepon)
        
        result['object'] = nasabah
        return result
    except:
        raise

def fetch_semua_user() -> list:
    '''

    Function ini nge-return semua user dalam database dalam bentuk object nasabah
    dengan nested object rekening (nasabah_contoh.rekening)

    '''
    try:
        query = '''
             SELECT n.nama, n.email, n.nomor_telepon, n.alamat, r.id_nasabah, r.nomor_rekening, r.jumlah_saldo
             FROM rekening r
             JOIN nasabah n ON r.id_nasabah = n.id
            '''       
        result = db.fetch(query, None)

        nasabah_arr: list[Nasabah] = []

        for row in result:
            ntemp = Nasabah(row[0], None, row[1], row[2], row[3], True)
            rtemp = Rekening(row[4], row[5], row[6])

            ntemp.rekening = rtemp

            nasabah_arr.append(ntemp)

        return nasabah_arr
    except:
        raise

def fetch_riwayat_transaksi(nomor_rekening: str):
    """
    Function untuk mengambil riwayat transaksi total user,

    nomor_rekening: str 

    return: array[RiwayatTransaksi]
    """
    query: str = 'SELECT nomor_rekening_sumber, nomor_rekening_tujuan, jenis_transaksi, jumlah_uang, datetime_transaksi FROM riwayat_transaksi WHERE nomor_rekening_sumber=%s OR nomor_rekening_tujuan=%s ORDER BY datetime_transaksi DESC'
    values: tuple = (nomor_rekening, nomor_rekening)

    result = db.fetch(query, values)
    rt_arr: list[RiwayatTransaksi] = []

    for row in result:
        rt_arr.append(
            RiwayatTransaksi(row[0], row[1], row[2], row[3], row[4].strftime('%Y-%m-%d %H:%M:%S'))
        )

    return rt_arr

def fetch_aliran_uang(nomor_rekening: str):
    """
    Function untuk mengambil aliran uang total user dibagi bulanan

    nomor_rekening: str 

    return: array[dict[dict]]
        dict: 'month_key': { 'total_uang_masuk': number, 'total_uang_keluar': number }
        example: '2025-11': { 'total_uang_masuk': 20000, 'total_uang_keluar': 15000 }
    """
    rt_arr = fetch_riwayat_transaksi(nomor_rekening)

    monthly_aliran = defaultdict(lambda: {'total_uang_masuk': 0, 'total_uang_keluar': 0})

    for rt in rt_arr:
        month_key = rt.datetime_transaksi.strftime('%Y-%m')

        match rt.jenis_transaksi:
            case StringJenisTransaksi.DEPOSIT:
                monthly_aliran[month_key]['total_uang_masuk'] += rt.jumlah_uang
            case StringJenisTransaksi.WITHDRAW:
                monthly_aliran[month_key]['total_uang_keluar'] += rt.jumlah_uang
            case StringJenisTransaksi.TRANSFER:
                if(rt.nomor_rekening_tujuan == nomor_rekening):
                    monthly_aliran[month_key]['total_uang_masuk'] += rt.jumlah_uang
                else:
                    monthly_aliran[month_key]['total_uang_keluar'] += rt.jumlah_uang

    return monthly_aliran

def login_admin(token: str):
    """
    Function ini digunakan untuk login admin lewat admin token dalam database

    token: str 

    return: 0 (int, code success)
        or an error:
            'status': Status.ERROR,
            'type': ErrorType.CREDENTIALS
            'message': 'Token admin salah'
    """

    query: str = 'SELECT token FROM admin';
    result = db.fetch(query)

    print('\n\n')
    print(token)
    print(result[0][0])

    if token == result[0][0]:
        return 0
    else:
        raise CredentialsError({
            'status': Status.ERROR,
            'type': ErrorType.CREDENTIALS,
            'message': 'Token admin salah'
        })


# TESTING CODE
print(fetch_aliran_uang('89556137620373224647'))
