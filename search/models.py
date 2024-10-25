from django.db import models

import uuid
class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    jenis_makanan = models.CharField(max_length=266)
    rating = models.FloatField()
    harga = models.IntegerField()
    jarak = models.FloatField()

    def __str__(self):
        return f"{self.nama} {self.jenis_makanan} {self.rating} {self.harga} {self.jarak}"
