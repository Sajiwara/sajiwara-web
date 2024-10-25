import os
import csv
from tipemakanan.models import Makanan

def runtipemakanan():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/jogja_dataset.csv")

    try:
        with open(path_file, "r", encoding="utf-8") as file:
            read = csv.DictReader(file)
            for row in read:
                preferensi = row['Preferensi Makanan'].strip()
                variasi = row['Variasi Makanan'].strip()
                restoran = row['Nama Restoran'].strip()

                # Cek apakah preferensi makanan sudah ada
                if not Makanan.objects.filter(preferensi=preferensi, menu=variasi, restoran=restoran).exists():
                    # Jika belum, buat instance baru dan simpan
                    makanan_obj = Makanan(preferensi=preferensi, menu=variasi, restoran=restoran)
                    makanan_obj.save()
                    print(f"Saved: {makanan_obj}")  # Print untuk konfirmasi penyimpanan
                else:
                    print(f"Already exists: {preferensi} - {variasi}")  # Print jika sudah ada
    except Exception as e:
        print(f"An error occurred: {e}")