import os
import csv
from wishlistmenu.models import Menu, Restaurant
from katalog.models import Restonya  # Menggunakan model Restonya

def import_menu_resto():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/jogja_dataset.csv")

    with open(path_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            menu_name = row['MENU'].strip()
            resto_name = row['RESTO YANG MENYEDIAKAN MENU'].strip()

            # Create or retrieve the restaurant instance
            restaurant, created = Restaurant.objects.get_or_create(name=resto_name)

            # Check and save the menu item, associating it with the restaurant
            if not Menu.objects.filter(menu=menu_name, restaurant=restaurant).exists():
                menu_item = Menu(menu=menu_name, restaurant=restaurant)
                print(menu_item)
                menu_item.save()

# Call the function to run the import
import_menu_resto()
