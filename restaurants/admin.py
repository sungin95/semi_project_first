from django.contrib import admin
from .models import Restaurants, Search

# Register your models here.


# Register your models here.
class RestaurantsAdmin(admin.ModelAdmin):
  list_display = ['restaurant_name', 'address', 'Opening_hours', 'menu', 'price_avg', 'parking', 'day_off', 'restaurant_phone_number', 'category']
  
class SearchAdmin(admin.ModelAdmin):
  list_display = ['keyword', 'count']
  
admin.site.register(Restaurants, RestaurantsAdmin)
admin.site.register(Search, SearchAdmin)