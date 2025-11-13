import mysql.connector
import re
import bcrypt

from database import connect_db
from rekening import Rekening
from CustomError import ValidationError, DatabaseError, Status, ErrorType, ValidationErrorCode

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

        validation_errors = Nasabah.validate_parameter(nama, password, email, nomor_telepon, alamat)
        if validation_errors:
            raise ValidationError({
                'status': Status.ERROR,
                'type': ErrorType.VALIDATION,
                'errors': errors
            })

        self.__nama = nama
        self.__password = Nasabah.hash_password(password)
        self.__email = email
        self.__nomor_telepon = nomor_telepon
        self.__alamat = alamat

        self.__id = self.create_in_database()

        self.rekening = Rekening(self.__id)
    
    @staticmethod
    def hash_password(password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def validate_parameter(
        nama: str,
        password: str,
        email: str,
        nomor_telepon: str,
        alamat: str
    ):
        errors = []

        email_duplicate_query = "SELECT * FROM nasabah WHERE email='%s'"
        email_duplicate_values = (email,)

        nomor_telepon_duplicate_query = "SELECT * FROM nasabah WHERE nomor_telepon='%s'"
        nomor_telepon_duplicate_values = (nomor_telepon,)

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

    def create_in_database(self):
        query = 'INSERT INTO nasabah (nama, password, email, nomor_telepon, alamat) VALUES (%s, %s, %s, %s, %s)'
        values = (self.__nama, self.__password, self.__email, self.__nomor_telepon, self.__alamat)

        try:
            last_row_id = db.exec_insert_query(query, values)

            return last_row_id
        except mysql.connector.IntegrityError as e:
            db.rollback()
            errno = e.errno

            if errno == db.DUPLICATE_ERRNO:
                field = str(e).split("for key '")[1].split("'")[0]

                raise DatabaseError({
                    'status': Status.ERROR,
                    'type': ErrorType.DATABASE,
                    'message': f'Tidak dapat membuat nasabah "{self.__nama}" dikarenakan "{field}" duplikat'
                })
            elif errno == db.NOT_NULL_ERRNO:
                field = str(e).split("Column '")[1].split("'")[0]

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