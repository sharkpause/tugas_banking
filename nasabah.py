from database import connect_db

from rekening import Rekening

db = connect_db()

class Nasabah:
    def __init__(self, nama: str, password: str, email: str, nomor_telepon: str, alamat: str):
        self.__nama = nama
        self.__password = password # belum di-hash
        self.__email = email
        self.__nomor_telepon = nomor_telepon
        self.__alamat = alamat

        self.__id = create_in_database()

        self.rekening = Rekening(self.__id)
    
    def create_in_database(self):
        query = 'INSERT INTO nasabah (nama, password, email, nomor_telepon, alamat) VALUES (%s, %s, %s, %s, %s)'
        values = (self.__nama, self.__password, self.__email, self.__nomor_telepon, self.__alamat)

        return db.exec_insert_query(query, values)

    def telepon(self):
        print(f'Sedang menghubung {self.__nama} ({self.__nomor_telepon})...')
    
    @property
    def nama(self) -> str:
        return self.__nama
    
    @property
    def email(self) -> str:
        return self.__email
    
    @property
    def nomor_telepon(self) -> str:
        return self.__nomor_telepon
    
    @property
    def alamat(self) -> str:
        return self.__alamat
    
    # def commit():
    #     pass