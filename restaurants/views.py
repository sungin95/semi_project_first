from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from .models import Restaurants
from .forms import RestaurantForm
from django.contrib import messages

# Create your views here.
def main(request):
    return render(request, 'restaurants/main.html')

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