from django.db import models
import uuid
# Create your models here.
class Restonya(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.CharField(max_length=266) # hasil data set
    preferensi = models.CharField(max_length=266)
    menu = models.CharField(max_length=1000, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    harga = models.IntegerField(null=True, blank=True)
    jarak = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.restaurant} {self.preferensi} {self.menu} {self.rating} {self.harga}{self.jarak}"
