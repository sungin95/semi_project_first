from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.template.defaultfilters import slugify

category_CHOICES = (
    ('한식', '한식'),
    ('양식', '양식'),
    ('중식', '중식'),
    ('일식', '일식'),
    ('기타', '기타'),
)

parking_CHOICES = (
    ('주차공간없음', '주차공간없음'),
    ('유료주차 가능', '유료주차 가능'),
    ('무료주차 가능', '무료주차 가능'),
    ('기타', '기타'),
)

# Create your models here.
class Restaurants(models.Model):
    restaurant_name = models.CharField(max_length=50)
    전화번호 = PhoneNumberField(blank=True)
    address = models.TextField()
    Opening_hours = models.TextField()
    menu = models.TextField()
    price_avg = models.TextField()
    day_off = models.CharField(max_length=40)
    parking = models.CharField(max_length=50, choices=parking_CHOICES)
    category = models.CharField(max_length=50, choices=category_CHOICES)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_restaurant"
    )
    hits = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    @property
    def click(self):
        self.hits += 1
        self.save()


class Search(models.Model):
    keyword = models.TextField(max_length=30)
    count = models.IntegerField(default=0)


def get_image_filename(instance, filename):
    slugs = slugify("title")
    # 제목 - 슬러그된 파일이름 형태
    return "post_images/%s-%s" % (slugs, filename)

class RestaurantImages(models.Model):
    restaurant = models.ForeignKey(
        Restaurants, default=None, on_delete=models.CASCADE, related_name="restaurant"
    )
    image = models.ImageField(upload_to=get_image_filename, blank=True)
    class Meta:
        # 단수
        verbose_name = "Image"
        # 복수
        verbose_name_plural = "Images"

