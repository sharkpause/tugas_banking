from __future__ import annotations

import random

from database import Database
from CustomClasses import DataChanges, Status, InsufficientFundsError, ErrorType

from utilitas import nomor_rekening_ke_Rekening

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
    
    Server developer tidak direkomendasikan untuk memanggil method create_in_database
    dikarenakan method itu membuat objek Rekening ke dalam database yang dapat
    memicu error yang tidak diekspektasi

    id_nasabah: ID nasabah
    nomor_rekening: Nomor rekening nasabah, jika tidak diisi, akan secara automatis diisikan dengan nomor rekening random baru
    jumlah_saldo: Jumlah saldo rekening, jika tidak diisi, akan secara automatis diisikan dengan 0 (nol)

    """

    def __init__(self, id_nasabah: int, nomor_rekening: str = generate_nomor_rekening(), jumlah_saldo: int = 0):
        self.__nomor_rekening: str = nomor_rekening
        self.__jumlah_saldo: int = jumlah_saldo
        
        self.__id_pemilik: int = id_nasabah
    
    def __create_in_database(self) -> Status.SUCCESS | Status.ERROR:
        query: str = 'INSERT INTO rekening (id_nasabah, nomor_rekening, jumlah_saldo) VALUES (%s, %s, %s)'
        values: tuple = (self.__id_pemilik, self.__nomor_rekening, self.__jumlah_saldo)

        db.exec_query(query, values)

        return Status.SUCCESS

    def tambah_saldo(self, jumlah_uang: int) -> Status.SUCCESS | Status.ERROR:
        self.__jumlah_saldo += jumlah_uang

        self.commit(DataChanges.JUMLAH_SALDO)

        return Status.SUCCESS
    
    def kurang_saldo(self, jumlah_uang: int) -> Status.SUCCESS | Status.ERROR:
        if jumlah_uang > self.__jumlah_saldo:
            raise InsufficientFundsError({
                'status': Status.ERROR,
                'type': ErrorType.INSUFFICIENT_FUNDS,
                'message': 'Saldo tidak mencukupi'
            })
        
        self.__jumlah_saldo -= jumlah_uang

        self.commit(DataChanges.JUMLAH_SALDO)

        return Status.SUCCESS
    
    @property
    def jumlah_saldo(self) -> int:
        return self.__jumlah_saldo
    
    @property
    def nomor_rekening(self) -> str:
        return self.__nomor_rekening
    
    @property
    def id_pemilik(self) -> int:
        return self.__id_pemilik
    
    def commit(self, changes: DataChanges) -> Status.SUCCESS | Status.ERROR:
        if changes == DataChanges.JUMLAH_SALDO:
            query: str = 'UPDATE rekening SET jumlah_saldo = %s WHERE nomor_rekening = %s'
            values: tuple = (self.__jumlah_saldo, self.__nomor_rekening)

            db.exec_query(query, values)
        
        return Status.SUCCESS