from __future__ import annotations
from datetime import datetime

from CustomClasses import Status, JenisTransaksi

from database import db

class RiwayatTransaksi:
    """

    RiwayatTransaksi merepresentasi row data dalam database dalam bentuk object
    untuk lebih mudah interaksi oleh server developer.
    
    Server developer tidak direkomendasikan untuk memodifikasi tabel riwayat_transaksi
    secara langsung dalam database.

    Ini tidak akan pernah perlu digunakan oleh server developer karena hanya
    di-call dalam fungsi transaksi() manager.py.
    Jangan membuat riwayat transaksi sendiri, semuanya sudah di-handle
    dalam manager.py

    nomor_rekening_sumber: string
    nomor_rekening_tujuan: string
    jenis_transaksi: Transaksi
    jumlah_uang: integer
    datetime_transaksi format:      YYYY-mm-dd HH:mm:ss
                       penjelasan:  Tahun-bulan-hari Jam:menit:detik
                       contoh:      2025-11-14 20:10:44
    
    """
    def __init__(self, nomor_rekening_sumber: str, nomor_rekening_tujuan: str, jenis_transaksi: JenisTransaksi, jumlah_uang: int, datetime_transaksi: str): 
        self.__nomor_rekening_sumber = nomor_rekening_sumber
        self.__nomor_rekening_tujuan = nomor_rekening_tujuan
        self.__jenis_transaksi = jenis_transaksi
        self.__jumlah_uang = jumlah_uang
        self.__datetime_transaksi = datetime.strptime(datetime_transaksi, "%Y-%m-%d %H:%M:%S")
    
    def __create_in_database(self) -> Status.SUCCESS | Status.ERROR:
        try:
            query: str = 'INSERT INTO riwayat_transaksi (nomor_rekening_sumber, nomor_rekening_tujuan, jenis_transaksi, jumlah_uang, datetime_transaksi) VALUES (%s, %s, %s, %s, %s)'
            val: tuple = (
                self.__nomor_rekening_sumber,
                self.__nomor_rekening_tujuan,
                self.__jenis_transaksi,
                self.__jumlah_uang,
                self.__datetime_transaksi
            )

            db.exec_insert_query(query, val)
            return Status.SUCCESS
        except Exception as e:
            db.rollback()
            raise DatabaseError({
                'status': Status.ERROR,
                'type': ErrorType.DATABASE,
                'message': f'Tidak dapat membuat riwayat transaksi'
            })
    
    @property
    def nomor_rekening_sumber(self) -> str:
        return self.__nomor_rekening_sumber

    @property
    def nomor_rekening_tujuan(self) -> str:
        return self.__nomor_rekening_tujuan

    @property
    def jenis_transaksi(self) -> str:
        return self.__jenis_transaksi

    @property
    def jumlah_uang(self) -> int:
        return self.__jumlah_uang

    @property
    def datetime_transaksi(self) -> str:
        return self.__datetime_transaksi

    def kesimpulan(self) -> str:
        return f'Pada {self.__datetime_transaksi} terjadi transaksi {self.__jenis_transaksi} dengan jumlah uang {self.__jumlah_uang} dari {self.__nomor_rekening_sumber} ke {self.__nomor_rekening_tujuan}'
    
    # def commit():
    #     pass

jenis_transaksi_mapper = {
    JenisTransaksi.DEPOSIT: 'deposit',
    JenisTransaksi.WITHDRAW: 'withdraw',
    JenisTransaksi.TRANSFER: 'transfer'
}

def new_RT(nomor_rekening_sumber: str, nomor_rekening_tujuan: str, jenis: JenisTransaksi, jumlah_uang: int, datetime_transaksi: str) -> RT:
    jenis = jenis_transaksi_mapper[jenis]

    rt = RiwayatTransaksi(nomor_rekening_sumber, nomor_rekening_tujuan, jenis, jumlah_uang, datetime_transaksi)
    rt._RiwayatTransaksi__create_in_database()