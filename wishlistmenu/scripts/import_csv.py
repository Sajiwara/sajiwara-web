import os
import csv
from wishlistresto.models import Restaurant, MenuItem

def import_menu_resto():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/menu_resto_jogja.csv")  # Sesuaikan path file

    with open(path_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            menu = row['MENU'].strip()
            resto_name = row['RESTO YANG MENYEDIAKAN MENU'].strip()

            # Cek dan simpan restoran
            restaurant, created = Restaurant.objects.get_or_create(name=resto_name)

            # Cek dan simpan menu item
            if not MenuItem.objects.filter(name=menu, restaurant=restaurant).exists():
                menu_item = MenuItem(name=menu, restaurant=restaurant)
                menu_item.save()
