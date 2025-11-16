from manager import deposit, transfer, withdraw, buat_nasabah_baru, tutup_nasabah
from database import db

def test_deposit(nasabah_don_in_db, nasabah_rachel_in_db):
    don_previous = nasabah_don_in_db.rekening.jumlah_saldo
    rachel_previous = nasabah_rachel_in_db.rekening.jumlah_saldo

    don_deposit = 20_000
    rachel_deposit = 30_000
    don_deposit_id = deposit(don_deposit, '2025-01-01 10:10:10', nasabah_don_in_db.rekening)
    rachel_deposit_id = deposit(rachel_deposit, '2024-02-02 20:20:20', nasabah_rachel_in_db.rekening)

    assert db.fetch('SELECT id_transaksi FROM riwayat_transaksi WHERE id_transaksi=%s', (don_deposit_id,)) is not None
    assert db.fetch('SELECT id_transaksi FROM riwayat_transaksi WHERE id_transaksi=%s', (rachel_deposit_id,)) is not None

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_previous + don_deposit
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_previous + rachel_deposit

def test_withdraw(nasabah_don_in_db, nasabah_rachel_in_db):
    don_deposit = 20_000
    rachel_deposit = 30_000
    deposit(don_deposit, '2025-01-01 10:10:10', nasabah_don_in_db.rekening)
    deposit(rachel_deposit, '2024-02-02 20:20:20', nasabah_rachel_in_db.rekening)

    don_withdraw = 10_000
    rachel_withdraw = 10_000
    don_withdraw_id = withdraw(don_withdraw, '2025-01-01 10:10:10', nasabah_don_in_db.rekening)
    rachel_withdraw_id = withdraw(rachel_withdraw, '2025-01-01 10:10:10', nasabah_rachel_in_db.rekening)

    assert db.fetch('SELECT id_transaksi FROM riwayat_transaksi WHERE id_transaksi=%s', (don_withdraw_id,)) is not None
    assert db.fetch('SELECT id_transaksi FROM riwayat_transaksi WHERE id_transaksi=%s', (rachel_withdraw_id,)) is not None

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_deposit - don_withdraw
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_deposit - rachel_withdraw

def test_transfer(nasabah_don_in_db, nasabah_rachel_in_db):
    don_deposit = 20_000
    rachel_deposit = 30_000

    deposit(don_deposit, '2025-01-01 10:10:10', nasabah_don_in_db.rekening)
    deposit(rachel_deposit, '2024-02-02 20:20:20', nasabah_rachel_in_db.rekening)

    transfer_amount = 15_000
    transfer_id = transfer(transfer_amount, '2025-01-01 10:10:10', nasabah_don_in_db.rekening, nasabah_rachel_in_db.rekening)
    assert db.fetch('SELECT id_transaksi FROM riwayat_transaksi WHERE id_transaksi=%s', (transfer_id,)) is not None

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_deposit - transfer_amount
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_deposit + transfer_amount