import uuid
from django.db import models
from django.contrib.auth.models import User

class WishlistMenu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Menggunakan UUID sebagai primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=255)  # Nama menu makanan
    resto_name = models.CharField(max_length=255)  # Nama resto yang menyediakan menu
    tried = models.BooleanField(default=False)  # Menu sudah dicoba atau belum

    def __str__(self):
        return f"Wishlist {self.user.username} - {self.menu_name} at {self.resto_name}"
