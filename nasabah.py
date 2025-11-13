import mysql.connector
import re

from database import connect_db
from rekening import Rekening
from CustomError import ValidationError

db = connect_db()

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PHONE_REGEX = r'^08\d{8,11}$'

class Nasabah:
    def __init__(self, nama: str, password: str, email: str, nomor_telepon: str, alamat: str):
        nama = nama.strip()
        password = password.strip()
        email = email.strip()
        nomor_telepon = nomor_telepon.strip()
        alamat = alamat.strip()

        errors = self.validate_parameter(nama, password, email, nomor_telepon, alamat)
        if(len(errors) == 0):
            raise ValidationError({
                'status': 'error',
                'errors': errors
            })

        self.__nama = nama
        self.__password = password # belum di-hash
        self.__email = email
        self.__nomor_telepon = nomor_telepon
        self.__alamat = alamat

        self.__id = self.create_in_database()

        self.rekening = Rekening(self.__id)
    
    def validate_parameter(
        self,
        nama: str,
        password: str,
        email: str,
        nomor_telepon: str,
        alamat: str
    ):
        errors = []

        if not nama:
            errors.append({'field': 'nama', 'code': 'EMPTY', 'message': 'Nama tidak bisa kosong'})
        if not password:
            errors.append({'field': 'password', 'code': 'EMPTY', 'message': 'Password tidak bisa kosong'})
        if not email:
            errors.append({'field': 'email', 'code': 'EMPTY', 'message': 'Email tidak bisa kosong'})
        elif not re.match(EMAIL_REGEX, email):
            errors.append({'field': 'email', 'code': 'INVALID_FORMAT', 'message': f'Format email {email} tidak benar'})
        if not nomor_telepon:
            errors.append({'field': 'nomor_telepon', 'code': 'EMPTY', 'message': 'Nomor telepon tidak bisa kosong'})
        elif not re.match(PHONE_REGEX, nomor_telepon):
            errors.append({'field': 'nomor_telepon', 'code': 'INVALID_FORMAT', 'message': f'Format nomor telepon {nomor_telepon} tidak benar'})
        if not alamat:
            errors.append({'field': 'alamat', 'code': 'EMPTY', 'message': 'Alamat tidak bisa kosong'})

        return errors

    def create_in_database(self):
        query = 'INSERT INTO nasabah (nama, password, email, nomor_telepon, alamat) VALUES (%s, %s, %s, %s, %s)'
        values = (self.__nama, self.__password, self.__email, self.__nomor_telepon, self.__alamat)

        try:
            last_row_id = db.exec_insert_query(query, values)
            db.commit()

            return last_row_id
        except mysql.connector.IntegrityError as e:
            db.rollback()

            errno = e.errno

            if errno == db.DUPLICATE_ERRNO:
                field = str(e).split('for key '')[1].split(''')[0]

                raise ValueError(f'Tidak dapat membuat nasabah "{self.__nama}" dikarenakan "{field}" duplikat')
            elif errno == db.NOT_NULL_ERRNO:
                field = str(e).split('Column '')[1].split(''')[0]
                raise ValueError(f'Tidak dapat membuat nasabah "{self.__nama}" dikarenakan "{field}" tidak boleh kosong')
            else:
                raise RuntimeError(f'Integrity error saat membuat nasabah.\n{e}')
        except Exception as e:
            raise RuntimeError(f'Error saat membuat nasabah.\n{e}')

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