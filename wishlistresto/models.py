import uuid
from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Resto(models.Model):
    restaurant = models.CharField(max_length=266)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    wanted_resto = models.BooleanField(default=False)
    visited = models.BooleanField(default=False) 
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.restaurant}"