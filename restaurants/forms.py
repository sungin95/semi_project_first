from django import forms
from django import forms
from .models import Restaurants

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurants
        fields = '__all__'
        labels = {
                'restaurant_name': '음식점명',
                'address': '주소',
                'Opening_hours': '영업시간',
                'menu': '메뉴',
                'price_avg': '가격대',
                'parking': '주차',
                'day_off': '휴일',
            }