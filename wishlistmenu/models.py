import json
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers

# Create your models here.
class Menu(models.Model):
    menu = models.CharField(max_length=266) # hasil data set
    def __str__(self):
        return f"{self.menu}"
    
class WishlistMenu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu_wanted = models.CharField(max_length=266, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    wanted_menu = models.BooleanField(default=False)
    tried = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.menu_wanted}"
    
    def show_wishlist():
        all_wishlist = WishlistMenu.objects.all()
        json_data = serializers.serialize('json', all_wishlist)

        print(json.dumps(json.loads(json_data), indent=4))