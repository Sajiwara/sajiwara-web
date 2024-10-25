from django.db import models

# Create your models here.
class Makanan(models.Model):
    preferensi = models.CharField(max_length=35)
    menu = models.CharField(max_length=255)
    restoran = models.CharField(max_length=255, default="Unknown Restaurant")

    def __str__(self):
        return f"{self.restoran} - {self.preferensi}: {self.menu}"