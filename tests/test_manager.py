from manager import deposit, transfer, withdraw, buat_nasabah_baru, tutup_nasabah

def test_deposit(nasabah_don_in_db, nasabah_rachel_in_db):
    don_previous = nasabah_don_in_db.rekening.jumlah_saldo
    rachel_previous = nasabah_rachel_in_db.rekening.jumlah_saldo

    don_deposit = 20_000
    rachel_deposit = 30_000
    deposit(don_deposit, '2025-01-01 10:10:10', nasabah_don_in_db.rekening)
    deposit(rachel_deposit, '2024-02-02 20:20:20', nasabah_rachel_in_db.rekening)

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_previous + don_deposit
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_previous + rachel_deposit

def test_withdraw(nasabah_don_in_db, nasabah_rachel_in_db):
    don_previous = nasabah_don_in_db.rekening.jumlah_saldo
    rachel_previous = nasabah_rachel_in_db.rekening.jumlah_saldo

    don_deposit = 20_000
    rachel_deposit = 30_000
    deposit(don_deposit, '2025-01-01 10:10:10', nasabah_don_in_db.rekening)
    deposit(rachel_deposit, '2024-02-02 20:20:20', nasabah_rachel_in_db.rekening)

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_previous + don_deposit
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_previous + rachel_deposit