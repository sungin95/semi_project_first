from django import forms
from .models import Restaurants
from phonenumber_field.formfields import PhoneNumberField
from .models import RestaurantImages
from django.utils.translation import gettext_lazy as _


class RestaurantForm(forms.ModelForm):
    전화번호 = PhoneNumberField(
        region="KR",
        required=False,
    )

    class Meta:
        model = Restaurants
        fields = "__all__"
        widgets = {
            "menu": forms.Textarea(
                attrs={
                    "placeholder": "메뉴 - 가격, 형식으로 적어주세요. 예시) 탕수육(소) - 10000원, 탕수육(중) - 20000원, 탕수육(대) - 30000원",
                }
            ),
        }
        exclude = ["like_users", "user", "hits", "address"]
        labels = {
            "restaurant_name": "음식점명",
            "Opening_hours": "영업시간",
            "menu": "메뉴",
            "price_avg": "가격대",
            "parking": "주차",
            "day_off": "휴일",
            "category": "카테고리",
            "image": "가게 썸네일",
        }


class RestaurantImageForm(forms.ModelForm):
    class Meta:
        model = RestaurantImages
        fields = ("image",)
        labels = {
            "image": _("Image"),
        }
