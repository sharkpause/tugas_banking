import random

from database import create_db
db = create_db()

class Rekening:
    def generate_nomor_rekening(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(20))

    def __init__(self, id_nasabah: int):
        self.__changes = { # Logic tracking changes palingan diubah menjadi passing parameter tetapi untuk sekarang menggunakan dict
            'jumlah_saldo': False
        }

        self.__nomor_rekening = self.generate_nomor_rekening()
        self.__jumlah_saldo = 0
        
        self.__id_pemilik = id_nasabah

        query = 'INSERT INTO rekening (id_nasabah, nomor_rekening, jumlah_saldo) VALUES (%s, %s, %s)'
        values = (self.__id_pemilik, self.__nomor_rekening, self.__jumlah_saldo)

        db.exec_query(query, values)
    
    def tambah_saldo(self, jumlah_uang: int):
        self.__jumlah_saldo += jumlah_uang
        self.__changes['jumlah_saldo'] = True

        self.commit()
    
    def kurang_saldo(self, jumlah_uang: int):
        self.__jumlah_saldo -= jumlah_uang
        self.__changes['jumlah_saldo'] = True

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
    
    def commit(self):
        if self.__changes['jumlah_saldo']:
            query = 'UPDATE rekening SET jumlah_saldo = %s WHERE nomor_rekening = %s'
            values = (self.__jumlah_saldo, self.__nomor_rekening)

            db.exec_query(query, values)