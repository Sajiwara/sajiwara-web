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
            # food_preference = row['Preferensi Makanan'].strip()
            # location = float(row['Lokasi Restoran'].replace("km","").strip())
            # price_average = int(row['Harga Rata-Rata Makanan di Toko (Rp)'].strip())
            # rating = float(row['Rating Toko'].strip())
            # atmosphere_type = row['Jenis Suasana'].strip()
            # often_discount = row['Toko Sering Diskon (Ya/Tidak)'].strip().lower() == 'ya'
            # special_service_for_couples = row['Pelayanan Khusus Pasangan (Ya/Tidak)'].strip().lower() == 'ya'
            # entertainment = int(row['Entertainment'].strip())
            # crowd = int(row['Keramaian Restoran'].strip())
            # service_type = row['Disajikan atau Ambil Sendiri'].strip()
            # menu_type = row['All You Can Eat atau Ala Carte'].strip()

            # Create or retrieve the restaurant instance
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_name,
                # food_preference=food_preference,
                # location=location,
                # price_average=price_average,
                # rating=rating,
                # atmosphere_type=atmosphere_type,
                # often_discounted=often_discount,
                # special_service_for_couples=special_service_for_couples,
                # entertainment=entertainment,
                # crowd=crowd,
                # service_type=service_type,
                # menu_type=menu_type
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
