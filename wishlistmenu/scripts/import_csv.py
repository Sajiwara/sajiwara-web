import os
import csv
from wishlistmenu.models import Menu

def runwishlistmenu():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/jogja_dataset.csv")

    with open(path_file, "r") as file:
        read = csv.DictReader(file)
        for row in read:
            # Mengambil nama restoran dan menu dari file CSV
            restoran = row['Nama Restoran'].strip()
            menu = row['Variasi Makanan'].strip()  # Sesuaikan nama kolom dengan yang ada di CSV

            # Cek apakah menu sudah ada untuk restoran ini, jika tidak tambahkan
            if not Menu.objects.filter(resto=restoran, menu=menu).exists():
                menu_obj = Menu(resto=restoran, menu=menu)
                menu_obj.save()