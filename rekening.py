import random

from database import connect_db
from CustomClasses import DataChanges

db = connect_db()

class Rekening:
    def __init__(self, id_nasabah: int):
        self.__nomor_rekening = Rekening.__generate_nomor_rekening()
        self.__jumlah_saldo = 0
        
        self.__id_pemilik = id_nasabah

        query = 'INSERT INTO rekening (id_nasabah, nomor_rekening, jumlah_saldo) VALUES (%s, %s, %s)'
        values = (self.__id_pemilik, self.__nomor_rekening, self.__jumlah_saldo)

        db.exec_query(query, values)
    
    @staticmethod
    def __generate_nomor_rekening(self) -> str:
        return ''.join(str(random.randint(0, 9)) for _ in range(20))

    def tambah_saldo(self, jumlah_uang: int) -> None:
        self.__jumlah_saldo += jumlah_uang
        self.__changes[DataChanges.JUMLAH_SALDO] = True

        self.commit()
    
    def kurang_saldo(self, jumlah_uang: int) -> None:
        self.__jumlah_saldo -= jumlah_uang
        self.__changes[DataChanges.JUMLAH_SALDO] = True

        self.commit()
    
    @property
    def saldo(self) -> int:
        return self.__jumlah_saldo
    
    @property
    def nomor_rekening(self) -> str:
        return self.__nomor_rekening
    
    @property
    def id_pemilik(self) -> int:
        return self.__id_pemilik
    
    def commit(self, changes) -> None:
        if changes == DataChanges.JUMLAH_SALDO:
            query = 'UPDATE rekening SET jumlah_saldo = %s WHERE nomor_rekening = %s'
            values = (self.__jumlah_saldo, self.__nomor_rekening)

            db.exec_query(query, values)