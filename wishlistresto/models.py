from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Resto(models.Model):
    restaurant = models.CharField(max_length=266)
    visited = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.restaurant}"