from __future__ import annotations

from database import Database

db = Database()

def nomor_rekening_ke_Rekening(nomor_rekening: str) -> Rekening:
    query: str = 'SELECT id_nasabah, nomor_rekening, jumlah_saldo FROM rekening WHERE nomor_rekening=%s'
    val: tuple = (nomor_rekening,)
    
    result: list[tuple] = db.fetch(query, val)

    return Rekening(result[0][0], result[0][1], result[0][2]) if len(result) > 0 else None

def nomor_telepon_ke_Rekening(nomor_telepon: str) -> Rekening:
    query: str = 'SELECT id, nomor_rekening, jumlah_saldo FROM rekening CROSS JOIN nasabah WHERE nomor_telepon=%s'
    val: tuple = (nomor_telepon,)

    result: list[tuple] = db.fetch(query, val)

    return Rekening(result[0][0], result[0][1], result[0][2]) if len(result) > 0 else None

def email_ke_Rekening(email: str) -> Rekening:
    query: str = 'SELECT id, nomor_rekening, jumlah_saldo FROM rekening CROSS JOIN nasabah WHERE email=%s'
    val: tuple = (email,)

    result: list[tuple] = db.fetch(query, val)[0]
    return Rekening(result[0], result[1], result[2])

# Testing

# x = nomor_rekening_ke_Rekening('34674875834793492200')
# print(x.id_pemilik, x.nomor_rekening, x.jumlah_saldo)

# y = nomor_telepon_ke_Rekening('081231231111')
# print(y.id_pemilik, y.nomor_rekening, y.jumlah_saldo)

# print(nomor_rekening_ke_Rekening('34674875834793492201'))