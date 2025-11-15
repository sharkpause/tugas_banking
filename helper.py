from __future__ import annotations

from database import db
from nasabah import Nasabah

def nomor_telepon_ke_Nasabah(nomor_telepon: str) -> Nasabah | None:
    query: str = 'SELECT nama, email, nomor_telepon, alamat FROM nasabah WHERE nomor_telepon=%s'
    val: tuple = (nomor_telepon,)

    result: list[tuple] = db.fetch(query, val)

    return Nasabah(result[0][0], None, result[0][1], result[0][2], result[0][3], True) if len(result) > 0 else None

def email_ke_Nasabah(email: str) -> Nasabah | None:
    query: str = 'SELECT nama, email, nomor_telepon, alamat FROM nasabah WHERE email=%s'
    val: tuple = (email,)

    result: list[tuple] = db.fetch(query, val)

    return Nasabah(result[0][0], None, result[0][1], result[0][2], result[0][3], True) if len(result) > 0 else None

def nomor_rekening_ke_Rekening(nomor_rekening: str) -> Rekening | None:
    query: str = 'SELECT id_nasabah, nomor_rekening, jumlah_saldo FROM rekening WHERE nomor_rekening=%s'
    val: tuple = (nomor_rekening,)
    
    result: list[tuple] = db.fetch(query, val)

    return Rekening(result[0][0], result[0][1], result[0][2]) if len(result) > 0 else None

def nomor_telepon_ke_Rekening(nomor_telepon: str) -> Rekening | None:
    query: str = 'SELECT id, nomor_rekening, jumlah_saldo FROM rekening CROSS JOIN nasabah WHERE nomor_telepon=%s'
    val: tuple = (nomor_telepon,)

    result: list[tuple] = db.fetch(query, val)

    return Rekening(result[0][0], result[0][1], result[0][2]) if len(result) > 0 else None

def email_ke_Rekening(email: str) -> Rekening | None:
    query: str = 'SELECT id, nomor_rekening, jumlah_saldo FROM rekening CROSS JOIN nasabah WHERE email=%s'
    val: tuple = (email,)

    result: list[tuple] = db.fetch(query, val)

    return Rekening(result[0][0], result[0][1], result[0][2]) if len(result) > 0 else None