import os
import csv
from tipemakanan.models import Makanan

def runtipemakanan():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/jogja_dataset.csv")

    with open(path_file, "r") as file:
        read = csv.DictReader(file)
        for row in read:
            preferensi = row['Preferensi Makanan'].strip()
            variasi = row['Variasi Makanan'].strip()

            # Cek apakah preferensi makanan sudah ada
            if not Makanan.objects.filter(preferensi=preferensi, menu=variasi).exists():
                # Jika belum, buat instance baru dan simpan
                makanan_obj = Makanan(preferensi=preferensi, menu=variasi)
                makanan_obj.save()
