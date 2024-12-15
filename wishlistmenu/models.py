import json
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers

# Model untuk Restoran, menyimpan informasi nama restoran
class Restaurant(models.Model):
    name = models.CharField(max_length=266)  # Nama restoran
    def __str__(self):
        return self.name

# Model untuk Menu, menyimpan informasi item menu dan menghubungkannya dengan restoran
class Menu(models.Model):
    menu = models.CharField(max_length=266)  # Nama item menu
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')  # Hubungan dengan restoran

    def __str__(self):
        return f"{self.menu} from {self.restaurant.name}"  # Nama menu dengan nama restoran

# Model untuk WishlistMenu, menyimpan informasi tentang menu yang diinginkan atau telah dicoba oleh pengguna
class WishlistMenu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu_wanted = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)  # Hubungan dengan Menu
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    wanted_menu = models.BooleanField(default=False)  # Apakah menu diinginkan
    tried = models.BooleanField(default=False)  # Apakah menu sudah dicoba

    def __str__(self):
        # Pastikan menangani kasus `None`
        menu_name = self.menu_wanted.menu if self.menu_wanted else "Unknown Menu"
        username = self.user.username if self.user else "Unknown User"
        return f"{menu_name} for {username}"

    def show_wishlist(self):
        all_wishlist = WishlistMenu.objects.all()
        json_data = serializers.serialize('json', all_wishlist)
        print(json.dumps(json.loads(json_data), indent=4))
