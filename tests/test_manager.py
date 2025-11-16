from manager import deposit, transfer, withdraw, buat_nasabah_baru, tutup_nasabah
from database import db

def test_deposit(nasabah_don_in_db, nasabah_rachel_in_db):
    don_previous = nasabah_don_in_db.rekening.jumlah_saldo
    rachel_previous = nasabah_rachel_in_db.rekening.jumlah_saldo

    don_deposit = 20_000
    don_datetime = '2025-01-01 10:10:10'
    rachel_deposit = 30_000
    rachel_datetime = '2024-02-02 20:20:20'
    don_deposit_id = deposit(don_deposit, don_datetime, nasabah_don_in_db.rekening)
    rachel_deposit_id = deposit(rachel_deposit, rachel_datetime, nasabah_rachel_in_db.rekening)

    query = 'SELECT id_transaksi, nomor_rekening_sumber, datetime_transaksi, jumlah_uang FROM riwayat_transaksi WHERE id_transaksi=%s'

    don_query = db.fetch(query, (don_deposit_id,))
    rachel_query = db.fetch(query, (rachel_deposit_id,))

    assert don_query is not None
    assert rachel_query is not None

    assert don_query[0][1] == nasabah_don_in_db.rekening.nomor_rekening
    assert don_query[0][2].strftime('%Y-%m-%d %H:%M:%S') == don_datetime
    assert don_query[0][3] == don_deposit

    assert rachel_query[0][1] == nasabah_rachel_in_db.rekening.nomor_rekening
    assert rachel_query[0][2].strftime('%Y-%m-%d %H:%M:%S') == rachel_datetime
    assert rachel_query[0][3] == rachel_deposit

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_previous + don_deposit
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_previous + rachel_deposit

def test_withdraw(nasabah_don_in_db, nasabah_rachel_in_db):
    don_deposit = 20_000
    don_datetime = '2025-01-01 10:10:10'
    rachel_deposit = 30_000
    rachel_datetime = '2025-01-01 10:10:10'

    deposit(don_deposit, don_datetime, nasabah_don_in_db.rekening)
    deposit(rachel_deposit, rachel_datetime, nasabah_rachel_in_db.rekening)

    don_withdraw = 10_000
    rachel_withdraw = 10_000

    don_withdraw_id = withdraw(don_withdraw, don_datetime, nasabah_don_in_db.rekening)
    rachel_withdraw_id = withdraw(rachel_withdraw, rachel_datetime, nasabah_rachel_in_db.rekening)

    query = 'SELECT id_transaksi, nomor_rekening_sumber, datetime_transaksi, jumlah_uang FROM riwayat_transaksi WHERE id_transaksi=%s'

    don_query = db.fetch(query, (don_withdraw_id,))
    rachel_query = db.fetch(query, (rachel_withdraw_id,))

    assert don_query is not None
    assert rachel_query is not None

    assert don_query[0][1] == nasabah_don_in_db.rekening.nomor_rekening
    assert don_query[0][2].strftime('%Y-%m-%d %H:%M:%S') == don_datetime
    assert don_query[0][3] == don_withdraw

    assert rachel_query[0][1] == nasabah_rachel_in_db.rekening.nomor_rekening
    assert rachel_query[0][2].strftime('%Y-%m-%d %H:%M:%S') == rachel_datetime
    assert rachel_query[0][3] == rachel_withdraw

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_deposit - don_withdraw
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_deposit - rachel_withdraw

def test_transfer(nasabah_don_in_db, nasabah_rachel_in_db):
    don_deposit = 20_000
    rachel_deposit = 30_000

    deposit(don_deposit, '2025-01-01 10:10:10', nasabah_don_in_db.rekening)
    deposit(rachel_deposit, '2024-02-02 20:20:20', nasabah_rachel_in_db.rekening)

    transfer_amount = 15_000
    transfer_datetime = '2025-01-01 10:10:10'
    transfer_id = transfer(transfer_amount, transfer_datetime, nasabah_don_in_db.rekening, nasabah_rachel_in_db.rekening)

    query = db.fetch('SELECT id_transaksi, nomor_rekening_sumber, nomor_rekening_tujuan, datetime_transaksi, jumlah_uang FROM riwayat_transaksi WHERE id_transaksi=%s', (transfer_id,))
    assert query is not None

    assert query[0][1] == nasabah_don_in_db.rekening.nomor_rekening
    assert query[0][2] == nasabah_rachel_in_db.rekening.nomor_rekening
    assert query[0][3].strftime('%Y-%m-%d %H:%M:%S') == transfer_datetime
    assert query[0][4] == transfer_amount

    assert nasabah_don_in_db.rekening.jumlah_saldo == don_deposit - transfer_amount
    assert nasabah_rachel_in_db.rekening.jumlah_saldo == rachel_deposit + transfer_amount

def test_tutup_nasabah(nasabah_don_in_db, nasabah_rachel_in_db):
    tutup_nasabah(nasabah_don_in_db.nomor_telepon)
    tutup_nasabah(nasabah_rachel_in_db.nomor_telepon)

    select = 'SELECT status_buka FROM nasabah WHERE nomor_telepon=%s'
    assert db.fetch(select, (nasabah_don_in_db.nomor_telepon,))[0][0] == False
    assert db.fetch(select, (nasabah_rachel_in_db.nomor_telepon,))[0][0] == False