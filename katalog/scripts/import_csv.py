import os
import csv
from katalog.models import Restonya

def runkatalog():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/jogja_dataset.csv")

    with open(path_file, "r") as file:
        read = csv.DictReader(file)
        for row in read:
            restoran = row['Nama Restoran'].strip()
            preferensi = row['Preferensi Makanan'].strip()
            menu = row['Variasi Makanan'].strip()
            rating = row['Rating Toko'].strip()
            harga =  row['Harga Rata-Rata Makanan di Toko (Rp)'].strip()
            jarak_str = row['Lokasi Restoran'].strip()
            jarak = float(jarak_str.replace(' km', '')) 

            if not Restonya.objects.filter(restaurant=restoran, preferensi=preferensi, menu=menu, rating=rating, harga=harga, jarak=jarak).exists():
                restoran_obj = Restonya(restaurant=restoran, preferensi=preferensi, menu=menu, rating=rating, harga=harga, jarak=jarak)
                print(restoran_obj)
                restoran_obj.save()