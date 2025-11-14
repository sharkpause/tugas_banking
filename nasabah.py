import mysql.connector
import re
import bcrypt

from typing import List, Dict, Tuple

from database import Database
from rekening import Rekening
from CustomClasses import ValidationError, DatabaseError, Status, ErrorType, ValidationErrorCode
from utilitas import nomor_telepon_ke_Rekening

db = Database()

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PHONE_REGEX = r'^08\d{8,11}$'

class Nasabah:
    """

    Nasabah merepresentasi row data dalam database dalam bentuk object
    untuk lebih mudah interaksi oleh server developer.
    
    Sudah meng-handle validation, password hashing, dan database interaction.
    
    Server developer tidak direkomendasikan untuk memodifikasi tabel nasabah
    secara langsung dalam database di luar method-method dalam class ini.

    """
    def __init__(self, nama: str, password: str, email: str, nomor_telepon: str, alamat: str):
        nama: str = nama.strip()
        password: str = password.strip()
        email: str = email.strip()
        nomor_telepon: str = nomor_telepon.strip()
        alamat: str = alamat.strip()

        validation_errors = Nasabah.__validate_parameter(nama, password, email, nomor_telepon, alamat)
        if validation_errors:
            raise ValidationError({
                'status': Status.ERROR,
                'type': ErrorType.VALIDATION,
                'errors': validation_errors
            })

        self.__nama: str = nama
        self.__password: str = Nasabah.__hash_password(password)
        self.__email: str = email
        self.__nomor_telepon: str = nomor_telepon
        self.__alamat: str = alamat

        try:
            self.rekening: Rekening = nomor_telepon_ke_Rekening(nomor_telepon_ke_Rekening)
        except:
            self.rekening: Rekening = None

    @staticmethod
    def __hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def __validate_parameter(
        nama: str,
        password: str,
        email: str,
        nomor_telepon: str,
        alamat: str
    ) -> List[Dict]:
        errors: List[Dict] = []

        email_duplicate_query: str = "SELECT * FROM nasabah WHERE email=%s"
        email_duplicate_values: Tuple = (email,)

        nomor_telepon_duplicate_query: str = "SELECT * FROM nasabah WHERE nomor_telepon=%s"
        nomor_telepon_duplicate_values: Tuple = (nomor_telepon,)

        if not nama:
            errors.append({
                'field': 'nama', 
                'code': ValidationErrorCode.EMPTY, 
                'message': 'Nama tidak bisa kosong'
            })

        if not password:
            errors.append({
                'field': 'password', 
                'code': ValidationErrorCode.EMPTY, 
                'message': 'Password tidak bisa kosong'
            })

        if not email:
            errors.append({
                'field': 'email', 
                'code': ValidationErrorCode.EMPTY, 
                'message': 'Email tidak bisa kosong'
            })
        elif not re.match(EMAIL_REGEX, email):
            errors.append({
                'field': 'email', 
                'code': ValidationErrorCode.INVALID_FORMAT, 
                'message': f'Format email {email} tidak benar'
            })
        elif db.fetch(email_duplicate_query, email_duplicate_values):
            errors.append({
                'field': 'email', 
                'code': ValidationErrorCode.DUPLICATE, 
                'message': 'Email sudah digunakan'
            })
            
        if not nomor_telepon:
            errors.append({
                'field': 'nomor_telepon', 
                'code': ValidationErrorCode.EMPTY,
                'message': 'Nomor telepon tidak bisa kosong'
            })
        elif not re.match(PHONE_REGEX, nomor_telepon):
            errors.append({
                'field': 'nomor_telepon',
                'code': ValidationErrorCode.INVALID_FORMAT,
                'message': f'Format nomor telepon {nomor_telepon} tidak benar'
            })
        elif db.fetch(nomor_telepon_duplicate_query, nomor_telepon_duplicate_values):
            errors.append({
                'field': 'nomor_telepon',
                'code': ValidationErrorCode.DUPLICATE,
                'message': 'Nomor telepon sudah digunakan'
            })

        if not alamat:
            errors.append({
                'field': 'alamat',
                'code': ValidationErrorCode.EMPTY,
                'message': 'Alamat tidak bisa kosong'
            })

        return errors

    def buat_rekening_baru(self) -> Status:
        if not self.__id:
            return { 'status': Status.ERROR, 'message': "Can't create a new rekening before a new nasabah in the database" }
        
        self.rekening = Rekening(self.__id)

    def __create_in_database(self) -> int:
        query: str = 'INSERT INTO nasabah (nama, password, email, nomor_telepon, alamat) VALUES (%s, %s, %s, %s, %s)'
        values: Tuple = (self.__nama, self.__password, self.__email, self.__nomor_telepon, self.__alamat)

        try:
            last_row_id: int = db.exec_insert_query(query, values)
            self.__id = last_row_id

            return Status.SUCCESS
        except mysql.connector.IntegrityError as e:
            db.rollback()
            errno: int = e.errno

            if errno == db.DUPLICATE_ERRNO:
                field: str = str(e).split("for key '")[1].split("'")[0]

                raise DatabaseError({
                    'status': Status.ERROR,
                    'type': ErrorType.DATABASE,
                    'message': f'Tidak dapat membuat nasabah "{self.__nama}" dikarenakan "{field}" duplikat'
                })
            elif errno == db.NOT_NULL_ERRNO:
                field: str = str(e).split("Column '")[1].split("'")[0]

                raise DatabaseError({
                    'status': Status.ERROR,
                    'type': ErrorType.DATABASE,
                    'message': f'Tidak dapat membuat nasabah "{self.__nama}" dikarenakan "{field}" tidak boleh kosong'
                })
            else:
                raise DatabaseError({
                    'status': Status.ERROR,
                    'type': ErrorType.DATABASE,
                    'message': f'Integrity error saat membuat nasabah.\n{e}'
                })
        except Exception as e:
            raise DatabaseError({
                'status': Status.ERROR,
                'type': ErrorType.DATABASE,
                'message': f'Error saat membuat nasabah.\n{e}'
            })


    def telepon(self) -> None:
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



# Testing
n = Nasabah('Don', '123', '123@321.com', '081331509015', 'Jl. Asia')
print(n.nama)