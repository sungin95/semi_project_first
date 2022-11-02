from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from .models import Restaurants
from .forms import RestaurantForm
from django.contrib import messages

# Create your views here.
def main(request):
    return render(request, 'restaurants/main.html')

def index(request):
    restaurants = Restaurants.objects.all()
    context = {
        'restaurants': restaurants,
    }
    return render(request, 'restaurants/index.html', context)

def detail(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_pk)
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'restaurants/detail.html', context)

def menu(request):
    return render(request, 'restaurants/menu.html')

@require_http_methods(['GET','POST'])
def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, files=request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.user = request.user
            restaurant.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('restaurants:main')
    form = RestaurantForm()
    context = {
        'form': form,
    }
    return render(request, 'restaurants/forms.html', context)

@require_http_methods(['GET','POST'])
def update(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurants:detail', restaurant.pk)
    else:
        form = RestaurantForm(instance=restaurant)
    context = {
        'restaurant': restaurant,
        'form': form,
    }
    return render(request, 'restaurants/forms.html', context)

def delete(request, restaurant_pk):
    get_object_or_404(Restaurants, pk=restaurant_pk).delete()
    return redirect('restaurants:main')