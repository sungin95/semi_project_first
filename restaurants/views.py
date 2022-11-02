from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurants

# Create your views here.
def main(request):
    return render(request, 'restaurants/main.html')

def detail(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_pk)
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'restaurants/detail.html')

def menu(request):
    return render(request, 'restaurants/menu.html')