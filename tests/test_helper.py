from helper import nomor_telepon_ke_Nasabah, email_ke_Nasabah, nomor_rekening_ke_Rekening, nomor_telepon_ke_Rekening, email_ke_Rekening

def test_nomor_telepon_ke_Nasabah(nasabah_in_db):
    result = nomor_telepon_ke_Nasabah(nasabah_in_db.nomor_telepon)
    assert result is not None
    assert nasabah_in_db.alamat == result.alamat
    assert nasabah_in_db.email == result.email
    assert nasabah_in_db.nama == result.nama
    assert nasabah_in_db.nomor_telepon == result.nomor_telepon

# def test_email_ke_Nasabah(nasabah_in_db):
#     result = email_ke_Nasabah(nasabah_in_db.email)
#     assert result is not None

# def test_nomor_rekening_ke_Rekening(nasabah_in_db):
#     result = nomor_rekening_ke_Rekening(nasabah_in_db.rekening.nomor_rekening)
#     assert result is not None

# def test_nomor_telepon_ke_rekening(nasabah_in_db):
#     result = nomor_telepon_ke_Rekening(nasabah_in_db.nomor_telepon)
#     assert result is not None