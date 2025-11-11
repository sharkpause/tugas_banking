# Rencana untuk sekarang untuk class ini adalah fetch data dari database dan mengubah ke class ini untuk admin viewing di UI
# jadi untuk sekarang tidak diperlukan

class RiwayatTransaksi:
    # datetime_transaksi format: YYYY-mm-dd HH:mm:ss
    def __init__(self, nomor_rekening_sumber: str, nomor_rekening_tujuan: str, jenis_transaksi: str, jumlah_uang: int, datetime_transaksi: str): 
        self.__nomor_rekening_sumber = nomor_rekening_sumber
        self.__nomor_rekening_tujuan = nomor_rekening_tujuan
        self.__jenis_transaksi = jenis_transaksi
        self.__jumlah_uang = jumlah_uang
        self.__datetime_transaksi = datetime_transaksi
    
    @property
    def nomor_rekening_sumber(self) -> str:
        return self.__nomor_rekening_sumber

    @property
    def nomor_rekening_tujuan(self) -> str:
        return self.__nomor_rekening_tujuan

    @property
    def jenis_transaksi(self) -> str:
        return self.__jenis_transaksi

    @property
    def jumlah_uang(self) -> int:
        return self.__jumlah_uang

    @property
    def datetime_transaksi(self) -> str:
        return self.__datetime_transaksi

    def kesimpulan(self):
        print(f'Pada {self.__datetime_transaksi} terjadi transaksi {self.__jenis_transaksi} dengan jumlah uang {self.__jumlah_uang} dari {self.__nomor_rekening_sumber} ke {self.__nomor_rekening_tujuan}')
    
    # def commit():
    #     pass