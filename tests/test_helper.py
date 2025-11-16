from helper import nomor_telepon_ke_Nasabah, email_ke_Nasabah, nomor_rekening_ke_Rekening, nomor_telepon_ke_Rekening, email_ke_Rekening

def test_nomor_telepon_ke_Nasabah(nasabah_don_in_db):
    result = nomor_telepon_ke_Nasabah(nasabah_don_in_db.nomor_telepon)
    assert result is not None
    assert nasabah_don_in_db.alamat == result.alamat
    assert nasabah_don_in_db.email == result.email
    assert nasabah_don_in_db.nama == result.nama
    assert nasabah_don_in_db.nomor_telepon == result.nomor_telepon

def test_email_ke_Nasabah(nasabah_rachel_in_db):
    result = email_ke_Nasabah(nasabah_rachel_in_db.email)
    assert result is not None
    assert nasabah_rachel_in_db.alamat == result.alamat
    assert nasabah_rachel_in_db.email == result.email
    assert nasabah_rachel_in_db.nama == result.nama
    assert nasabah_rachel_in_db.nomor_telepon == result.nomor_telepon

def test_nomor_rekening_ke_Rekening(nasabah_don_in_db):
    result = nomor_rekening_ke_Rekening(nasabah_don_in_db.rekening.nomor_rekening)
    assert result is not None
    assert nasabah_don_in_db.rekening.id_pemilik == result.id_pemilik
    assert nasabah_don_in_db.rekening.jumlah_saldo == result.jumlah_saldo
    assert nasabah_don_in_db.rekening.nomor_rekening == result.nomor_rekening

def test_nomor_telepon_ke_Rekening(nasabah_rachel_in_db):
    result = nomor_telepon_ke_Rekening(nasabah_rachel_in_db.nomor_telepon)

    assert result is not None
    assert nasabah_rachel_in_db.rekening.id_pemilik == result.id_pemilik
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == result.jumlah_saldo
    assert nasabah_rachel_in_db.rekening.nomor_rekening == result.nomor_rekening

def test_email_ke_Rekening(nasabah_rachel_in_db):
    result = email_ke_Rekening(nasabah_rachel_in_db.email)

    assert result is not None
    assert nasabah_rachel_in_db.rekening.id_pemilik == result.id_pemilik
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == result.jumlah_saldo
    assert nasabah_rachel_in_db.rekening.nomor_rekening == result.nomor_rekening