from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

category_CHOICES = (
    ('한식', '한식'),
    ('양식', '양식'),
    ('중식', '중식'),
    ('일식', '일식'),
    ('기타', '기타'),
)

# Create your models here.
class Restaurants(models.Model):
    restaurant_name = models.CharField(max_length=50)
    address = models.TextField()
    Opening_hours = models.TextField()
    menu = models.TextField()
    price_avg = models.TextField()
    parking = models.CharField(max_length=50)
    day_off = models.CharField(max_length=40)
    restaurant_phone_number = PhoneNumberField(blank=True)
    category = models.CharField(max_length=50, choices=category_CHOICES)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_restaurant"
    )
    
class Search(models.Model):
    keyword = models.TextField(max_length=30)
    count = models.IntegerField(default=0)
