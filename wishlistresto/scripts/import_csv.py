import os
import csv
from wishlistresto.models import Resto

def runwishlistresto():
    current_dir = os.path.dirname(__file__)
    path_file = os.path.join(current_dir, "../fixtures/jogja_dataset.csv")

    with open(path_file, "r") as file:
        read = csv.DictReader(file)
        for row in read:
            restoran = row['Nama Restoran']
            restoran = restoran.strip()

            if not Resto.objects.filter(restaurant=restoran).exists():
                restoran_obj = Resto(restaurant=restoran)
                restoran_obj.save()