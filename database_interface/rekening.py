from __future__ import annotations

import random

try:
    from database import db
    from CustomClasses import DataChanges, Status, InsufficientFundsError, ErrorType, JenisRekening, StringJenisRekening, DatabaseError
except:
    from .database import db
    from .CustomClasses import DataChanges, Status, InsufficientFundsError, ErrorType, JenisRekening, StringJenisRekening, DatabaseError

def generate_nomor_rekening() -> str:
    while True:
        n: str = ''.join(random.choices('0123456789', k=20))
        query: str = 'SELECT id_nasabah, nomor_rekening, jumlah_saldo FROM rekening WHERE nomor_rekening=%s'
        val: tuple = (n,)
        
        result: list[tuple] = db.fetch(query, val)
        if len(result) == 0:
            return n

class Rekening:
    """

    Rekening merepresentasi row data dalam database dalam bentuk object
    untuk lebih mudah interaksi oleh server developer.
    
    Server developer tidak direkomendasikan untuk memodifikasi tabel rekening
    secara langsung dalam database di luar method-method dalam class ini.
    
    Server developer tidak direkomendasikan untuk memanggil method create_in_database
    dikarenakan method itu membuat objek Rekening ke dalam database yang dapat
    memicu error yang tidak diekspektasi.

    Jika ingin membuat rekening baru yang untuk di-save ke dalam database, jangan.
    Itu sudah di-handle function buat_nasabah_baru() dalam manager.py.

    Gunakan function nomor_rekening_ke_Rekening, nomor_telepon_ke_Rekening, email_ke_Rekening
    untuk mendapatkan object Rekening untuk data di dalam database

    Jangan pernah call method increasing_balance dan decreasing_balance, selalu gunakan
    function transaksi dalam manager.py agar semua transaksi terekam dalam database

    id_nasabah: ID nasabah
    nomor_rekening: Nomor rekening nasabah, jika tidak diisi, akan secara automatis diisikan dengan None
    jumlah_saldo: Jumlah saldo rekening, jika tidak diisi, akan secara automatis diisikan dengan 0 (nol)

    """

    def __init__(self,
                 id_nasabah: int,
                 nomor_rekening: str | None = None,
                 jumlah_saldo: int = 0,
                 jenis_rekening: JenisRekening = JenisRekening.CHECKING):

        jenis_rekening_map = {
            JenisRekening.CHECKING: StringJenisRekening.CHECKING,
            JenisRekening.SAVINGS: StringJenisRekening.SAVINGS
        }
        self.__jenis_rekening = jenis_rekening_map[jenis_rekening]
        if nomor_rekening:
            self.__nomor_rekening: str = nomor_rekening
        else:
            self.__nomor_rekening: str = generate_nomor_rekening()
        
        self.__jumlah_saldo: int = jumlah_saldo
        
        self.__id_pemilik: int = id_nasabah
    
    def __create_in_database(self) -> Status:
        query: str = 'INSERT INTO rekening (id_nasabah, nomor_rekening, jumlah_saldo, jenis_rekening) VALUES (%s, %s, %s, %s)'
        
        while True: # Loop cuz generate_nomor_rekening might generate the same number
            self.__nomor_rekening = generate_nomor_rekening()
            val: tuple = (self.__id_pemilik, self.__nomor_rekening, self.__jumlah_saldo, self.__jenis_rekening)

            try:
                db.exec_insert_query(query, val)
                db.commit()
                break
            except mysql.connector.IntegrityError as e:
                if e.errno == db.DUPLICATE_ERRNO:
                    continue
                raise
            except:
                raise

        return Status.SUCCESS

    def __increase_balance(self, jumlah_uang: int) -> Status:
        self.__previous_saldo = self.__jumlah_saldo
        self.__jumlah_saldo += jumlah_uang

        self.__save_to_database(DataChanges.JUMLAH_SALDO)

        return Status.SUCCESS
    
    def __decrease_balance(self, jumlah_uang: int) -> Status:
        if jumlah_uang > self.__jumlah_saldo:
            raise InsufficientFundsError({
                'status': Status.ERROR,
                'type': ErrorType.INSUFFICIENT_FUNDS,
                'message': 'Saldo tidak mencukupi'
            })
        
        self.__previous_saldo = self.__jumlah_saldo
        self.__jumlah_saldo -= jumlah_uang

        self.__save_to_database(DataChanges.JUMLAH_SALDO)

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
    
    def __save_to_database(self, changes: DataChanges):
        try:
            if changes == DataChanges.JUMLAH_SALDO:
                query: str = 'UPDATE rekening SET jumlah_saldo = %s WHERE nomor_rekening = %s'
                values: tuple = (self.__jumlah_saldo, self.__nomor_rekening)

                db.exec_query(query, values)

            return Status.SUCCESS

        except Exception as e:
            db.rollback()
            self.__jumlah_saldo = self.__previous_saldo
            raise DatabaseError(f'Commit failed: {e}')
