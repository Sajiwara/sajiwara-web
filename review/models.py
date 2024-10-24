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
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    restaurant = models.ForeignKey(Restor, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True, null=True)  # Allow existing rows to remain blank

    def __str__(self):
        return f"Review by {self.user} on {self.date_posted}"