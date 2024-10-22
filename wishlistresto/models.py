import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Resto(models.Model):
    restaurant = models.CharField(max_length=266) # hasil data set
    def __str__(self):
        return f"{self.restaurant}"
    
class WishlistResto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant_wanted = models.CharField(max_length=266, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    wanted_resto = models.BooleanField(default=False)
    visited = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.restaurant_wanted}"
