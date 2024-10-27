import json
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers

class Restaurant(models.Model):
    name = models.CharField(max_length=266)  # Field for restaurant name
    def __str__(self):
        return self.name

class Menu(models.Model):
    menu = models.CharField(max_length=266)  # Menu item name
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')  # Associate menu with a restaurant

    def __str__(self):
        return f"{self.menu} from {self.restaurant.name}"  # Including restaurant name for clarity

class WishlistMenu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu_wanted = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)  # Link to Menu
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    wanted_menu = models.BooleanField(default=False)
    tried = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.menu_wanted} for {self.user.username}"  # More descriptive

    def show_wishlist(self):
        all_wishlist = WishlistMenu.objects.all()
        json_data = serializers.serialize('json', all_wishlist)
        print(json.dumps(json.loads(json_data), indent=4))
