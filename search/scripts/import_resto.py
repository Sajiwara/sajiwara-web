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

            if not Restaurant.objects.filter(nama=restoran,jenis_makanan =jenis,rating = rating).exists():
                restoran_obj = Restaurant(nama=restoran,jenis_makanan=jenis,rating=rating)
                restoran_obj.save()