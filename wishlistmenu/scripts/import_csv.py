import os
import csv
from wishlistmenu.models import Menu, Restaurant

def import_menu_resto():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/jogja_dataset.csv")

    with open(path_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            restaurant_name = row['Nama Restoran'].strip()

            # Create or retrieve the restaurant instance
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_name,
            )

            list_menu = row['Variasi Makanan'].strip().split(',')
            for menu in list_menu:
                menu_name = menu.strip()
                if not Menu.objects.filter(menu=menu_name, restaurant=restaurant).exists() and menu_name != "":
                    menu_item = Menu(menu=menu_name, restaurant=restaurant)
                    print(menu_item)
                    menu_item.save()

# Call the function to run the import
import_menu_resto()
