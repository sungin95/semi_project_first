from django.db import models

# Create your models here.
class Restaurants(models.Model):
    restaurant_name = models.CharField(max_length=50)
    address = models.TextField()
    Opening_hours = models.TextField()