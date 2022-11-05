from django import forms
from .models import Restaurants
from phonenumber_field.formfields import PhoneNumberField
from .models import RestaurantImages
from django.utils.translation import gettext_lazy as _

class RestaurantForm(forms.ModelForm):
    restaurant_phone_number = PhoneNumberField(
        region="KR",
        required=False,
    )
    class Meta:
        model = Restaurants
        fields = '__all__'
        exclude = ['like_users','user','hits',]
        labels = {
                'restaurant_name': '음식점명',
                'address': '주소',
                'Opening_hours': '영업시간',
                'menu': '메뉴',
                'price_avg': '가격대',
                'parking': '주차',
                'day_off': '휴일',
                'restaurant_phone_number': '전화번호',
                'category': '카테고리',
            }

class RestaurantImageForm(forms.ModelForm): 
    class Meta:
        model = RestaurantImages
        fields = ("image",)
        labels = {
            "image": _("Image"),
        }
