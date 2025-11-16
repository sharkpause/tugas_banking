import pytest
import uuid, random

from helper import nomor_telepon_ke_Nasabah, email_ke_Nasabah, nomor_rekening_ke_Rekening, nomor_telepon_ke_Rekening, email_ke_Rekening
from manager import buat_nasabah_baru, tutup_nasabah
from database import db

created_nasabah = []

def delete_nasabah(nomor_telepon: str = None, email: str = None):
    try:
        db.exec_query('SET FOREIGN_KEY_CHECKS = 0;')
        if nomor_telepon:
            query: str = 'DELETE FROM nasabah WHERE nomor_telepon = %s'
            val: tuple = (nomor_telepon,)

            db.exec_query(query, val)
            db.commit()
        elif email:
            query: str = 'DELETE FROM nasabah WHERE email = %s'
            val: tuple = (email,)

            db.exec_query(query, val)
            db.commit()
    except:
        db.rollback()
        raise

@pytest.fixture
def nasabah_don_in_db():
    unique_phone = "0819" + ''.join(random.choices('0123456789', k=8))
    unique_email = f"don_{uuid.uuid4().hex[:6]}@finfeed.com"

    nasabah = buat_nasabah_baru('Don', 'password', unique_email, unique_phone, 'Jl. Asia')

    created_nasabah.append(nasabah.nomor_telepon)

    yield nasabah

    delete_nasabah(unique_phone)

@pytest.fixture
def nasabah_rachel_in_db():
    unique_phone = "08" + ''.join(random.choices('0123456789', k=11))
    unique_email = f"rachel_{uuid.uuid4().hex[:6]}@sharkware.com"

    nasabah = buat_nasabah_baru('Rachel', 'password', unique_email, unique_phone, 'Jl. Asia')
    
    yield nasabah

    delete_nasabah(unique_phone)