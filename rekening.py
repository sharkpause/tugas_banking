import random

from typing import Tuple

from database import Database
from CustomClasses import DataChanges

db = Database()

def generate_nomor_rekening() -> str:
    while True:
        n = ''.join(random.choices('0123456789', k=20))
        if not nomor_rekening_ke_Rekening(n):
            return n

class Rekening:
    """
    Rekening merepresentasi row data dalam database dalam bentuk object
    untuk lebih mudah interaksi oleh server developer.
    
    Server developer tidak direkomendasikan untuk memodifikasi tabel rekening
    secara langsung dalam database di luar method-method dalam class ini.

    id_nasabah: ID nasabah
    nomor_rekening: Nomor rekening nasabah, jika tidak diisi, akan secara automatis diisikan dengan nomor rekening random baru
    jumlah_saldo: Jumlah saldo rekening, jika tidak diisi, akan secara automatis diisikan dengan 0 (nol)
    """

    def __init__(self, id_nasabah: int, nomor_rekening: str = generate_nomor_rekening(), jumlah_saldo: int = 0):
        self.__nomor_rekening: str = nomor_rekening
        self.__jumlah_saldo: int = jumlah_saldo
        
        self.__id_pemilik: int = id_nasabah
    
    def __create_in_database(self):
        query: str = 'INSERT INTO rekening (id_nasabah, nomor_rekening, jumlah_saldo) VALUES (%s, %s, %s)'
        values: Tuple = (self.__id_pemilik, self.__nomor_rekening, self.__jumlah_saldo)

        db.exec_query(query, values)

    def tambah_saldo(self, jumlah_uang: int) -> None:
        self.__jumlah_saldo += jumlah_uang

        self.commit(DataChanges.JUMLAH_SALDO)
    
    def kurang_saldo(self, jumlah_uang: int) -> None:
        self.__jumlah_saldo -= jumlah_uang

        self.commit(DataChanges.JUMLAH_SALDO)
    
    @property
    def jumlah_saldo(self) -> int:
        return self.__jumlah_saldo
    
    @property
    def nomor_rekening(self) -> str:
        return self.__nomor_rekening
    
    @property
    def id_pemilik(self) -> int:
        return self.__id_pemilik
    
    def commit(self, changes: DataChanges) -> None:
        if changes == DataChanges.JUMLAH_SALDO:
            query: str = 'UPDATE rekening SET jumlah_saldo = %s WHERE nomor_rekening = %s'
            values: Tuple = (self.__jumlah_saldo, self.__nomor_rekening)

            db.exec_query(query, values)