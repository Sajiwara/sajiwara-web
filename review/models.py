from django.db import models
import uuid
from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Restor(models.Model):
    restaurant = models.CharField(max_length=266)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.restaurant}, {self.rating}"