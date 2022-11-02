from django.db import models

# Create your models here.
class Restaurants(models.Model):
    restaurant_name = models.CharField(max_length=50)
    address = models.TextField()
    Opening_hours = models.TextField()
    menu = models.TextField()
    price_avg = models.TextField()
    parking = models.CharField(max_length=50)
    day_off = models.CharField(max_length=40)