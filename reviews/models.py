from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from django.utils import timezone
from django.template.defaultfilters import slugify


class Review(models.Model):
    restaurants = models.ForeignKey("restaurants.Restaurants", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_reviews")
    grade = models.FloatField(
        default=1, validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    # object 를 Post 의 title 문자열로 반환
    def __str__(self):
        return self.title

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return "방금 전"
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + "분 전"
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + "시간 전"
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + "일 전"
        else:
            return False


# image file naming
# instance => 현재 정의된 모델의 인스턴스
# filename => 파일에 원래 제공된 파일 이름. 이것은 최종 목적지 경로를 결정할 때 고려되거나 고려되지 않을 수 있음
def get_image_filename(instance, filename):
    # 해당 Post 모델의 title 을 가져옴
    # title = instance.post.title
    # slug - 의미있는 url 사용을 위한 필드.
    # slugfy 를 사용해서 title을 slug 시켜줌.
    slug = slugify("title")
    # 제목 - 슬러그된 파일이름 형태
    return "post_images/%s-%s" % (slug, filename)


class ReviewImages(models.Model):
    review = models.ForeignKey(
        Review, default=None, on_delete=models.CASCADE, related_name="image"
    )
    image = models.ImageField(upload_to=get_image_filename)
    # admin 에서 모델이름
    class Meta:
        # 단수
        verbose_name = "Image"
        # 복수
        verbose_name_plural = "Images"

    # 이것도 역시 post title 로 반환
    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
