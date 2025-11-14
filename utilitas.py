from typing import Tuple

from rekening import Rekening
from database import Database

db = Database()

def nomor_rekening_ke_Rekening(nomor_rekening: str) -> Rekening:
    query: str = 'SELECT id_nasabah, nomor_rekening, jumlah_saldo FROM rekening WHERE nomor_rekening=%s'
    val: Tuple = (nomor_rekening,)
    
    result: List[Tuple] = db.fetch(query, val)[0]
    return Rekening(result[0], result[1], result[2])

def nomor_telepon_ke_Rekening(nomor_telepon: str) -> Rekening:
    query: str = 'SELECT id, nomor_rekening, jumlah_saldo FROM rekening CROSS JOIN nasabah WHERE nomor_telepon=%s'
    val: Tuple = (nomor_telepon,)

    result: List[Tuple] = db.fetch(query, val)[0]
    return Rekening(result[0], result[1], result[2])

def email_ke_Rekening(email: str) -> Rekening:
    query: str = 'SELECT id, nomor_rekening, jumlah_saldo FROM rekening CROSS JOIN nasabah WHERE email=%s'
    val: Tuple = (email,)

    result: List[Tuple] = db.fetch(query, val)[0]
    return Rekening(result[0], result[1], result[2])

# Testing

# x = nomor_rekening_ke_Rekening('34674875834793492200')
# print(x.id_pemilik, x.nomor_rekening, x.jumlah_saldo)

# y = nomor_telepon_ke_Rekening('081231231111')
# print(y.id_pemilik, y.nomor_rekening, y.jumlah_saldo)