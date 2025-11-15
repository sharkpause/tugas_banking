import pytest

from helper import nomor_telepon_ke_Nasabah, email_ke_Nasabah, nomor_rekening_ke_Rekening, nomor_telepon_ke_Rekening, email_ke_Rekening
from manager import buat_nasabah_baru, hapus_nasabah

@pytest.fixture
def nasabah_in_db():
    nasabah = buat_nasabah_baru('Don', 'password', 'email@email.com', '081221122112', 'Jl. Asia')

    yield nasabah

    hapus_nasabah(nasabah.nomor_telepon)