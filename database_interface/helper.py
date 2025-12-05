from __future__ import annotations

try:
    from database import db
    from nasabah import Nasabah
    from rekening import Rekening
    from CustomClasses import StringJenisRekening, JenisRekening
except:
    from .database import db
    from .nasabah import Nasabah
    from .rekening import Rekening
    from .CustomClasses import StringJenisRekening, JenisRekening

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

def nomor_rekening_ke_Rekening(nomor_rekening: str) -> Rekening:
    query = 'SELECT id_nasabah, nomor_rekening, jumlah_saldo, jenis_rekening, status_buka FROM rekening WHERE nomor_rekening=%s'
    val = (nomor_rekening,)
    
    result = db.fetch(query, val)[0]

    jenis_rekening_map = {
        StringJenisRekening.CHECKING: JenisRekening.CHECKING,
        StringJenisRekening.SAVINGS: JenisRekening.SAVINGS
    }

    return Rekening(result[0], result[1], result[2], jenis_rekening_map[result[3]], result[4])


def nomor_telepon_ke_Rekening(nomor_telepon: str) -> list[Rekening]:
    query = '''
      SELECT r.id_nasabah, r.nomor_rekening, r.jumlah_saldo, r.jenis_rekening, r.status_buka
      FROM rekening r
      JOIN nasabah n ON r.id_nasabah = n.id
      WHERE n.nomor_telepon = %s
    '''
    val = (nomor_telepon,)
    results = db.fetch(query, val)
    return [Rekening(r[0], r[1], r[2], r[3], r[4]) for r in results]


def email_ke_Rekening(email: str) -> list[Rekening]:
    query = '''
      SELECT r.id_nasabah, r.nomor_rekening, r.jumlah_saldo, r.jenis_rekening, r.status_buka
      FROM rekening r
      JOIN nasabah n ON r.id_nasabah = n.id
      WHERE n.email = %s
    '''
    val = (email,)
    results = db.fetch(query, val)
    return [Rekening(r[0], r[1], r[2], r[3], r[4]) for r in results]

