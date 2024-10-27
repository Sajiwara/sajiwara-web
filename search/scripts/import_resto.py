import os
import csv
from search.models import Restaurant

def runsearch():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../data/jogja.csv")

    with open(path_file, "r") as file:
        read = csv.DictReader(file)
        for row in read:
            restoran = row['Nama Restoran']
            restoran = restoran.strip()

            jenis = row['Preferensi Makanan']
            jenis = jenis.strip()

            rating = row['Rating Toko']
            rating = rating.strip()

            harga = row['Harga Rata-Rata Makanan di Toko (Rp)']
            harga = harga.strip()

            jarak_str = row['Lokasi Restoran'].strip()
            jarak = float(jarak_str.replace(' km', '')) 

            suasana = row['Jenis Suasana']
            suasana = suasana.strip()

            entertainment = row['Entertainment']
            entertainment = entertainment.strip()

            keramaian = row['Keramaian Restoran']
            keramaian = keramaian.strip()

            
            if not Restaurant.objects.filter(nama=restoran,jenis_makanan =jenis,rating = rating,harga=harga,jarak=jarak,suasana=suasana,entertainment=entertainment,keramaian=keramaian).exists():
                restoran_obj = Restaurant(nama=restoran,jenis_makanan=jenis,rating=rating,harga=harga,jarak=jarak,suasana=suasana,entertainment=entertainment,keramaian=keramaian)
                restoran_obj.save()