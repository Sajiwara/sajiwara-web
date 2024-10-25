
import os
import csv
from review.models import Restor

def insertdata():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/places_to_eat_in_the_jogja_region - places_to_eat_in_the_jogja_region.csv")

    with open(path_file, "r") as file:
        read = csv.DictReader(file)
        for row in read:
            restoran = row['Nama Restoran']
            rating = row['Rating Toko']
            restoran = restoran.strip()

            if not Restor.objects.filter(restaurant=restoran).exists():
                restoran_obj = Restor(restaurant=restoran,rating=rating)
                restoran_obj.save()