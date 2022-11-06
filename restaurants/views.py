from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import (
    require_safe,
    require_http_methods,
    require_POST,
)
from django.contrib.auth.decorators import login_required
from .models import Restaurants, Search, RestaurantImages
from .forms import RestaurantForm, RestaurantImageForm
from django.contrib import messages
from reviews.models import Review
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator
from reviews.forms import CommentForm
from django.http import JsonResponse
from django.forms import modelformset_factory


# Create your views here.
def main(request):
    s = Search.objects.filter().order_by("-count")[:3]
    m = Search.objects.filter().order_by("count")[1:12]
    context = {
        "s": s,
        "m": m,
    }
    return render(request, "restaurants/main.html", context)


def index(request):
    restaurants = Restaurants.objects.all()
    context = {
        "restaurants": restaurants,
    }
    return render(request, "restaurants/index.html", context)


def detail(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_pk)
    reviews = restaurant.review_set.all()
    # k = Review.objects.order_by("id")
    page = request.GET.get("page", "1")
    paginator = Paginator(reviews, 3)
    page_obj = paginator.get_page(page)
    comment_form = CommentForm()
    cnt = 0
    add = 0
    for review in reviews:
        cnt += 1
        add += review.grade
    if cnt == 0:
        grade = ""
    else:
        grade = round(add / cnt, 1)
    context = {
        "restaurant": restaurant,
        "grade": grade,
        "reviews": reviews,
        "question_list": page_obj,
        "comment_form": comment_form,
    }
    return render(request, "restaurants/detail.html", context)


def menu(request):
    category = request.GET.get("category")
    restaurants = Restaurants.objects.filter(category=category)
    context = {
        "category": category,
        "restaurants": restaurants,
    }
    return render(request, "restaurants/menu.html", context)


@require_http_methods(["GET", "POST"])
def create(request):
    ImageFormSet = modelformset_factory(
        RestaurantImages, form=RestaurantImageForm, extra=5
    )
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        address = request.POST.get("address")
        formset = ImageFormSet(
            request.POST, request.FILES, queryset=RestaurantImages.objects.none()
        )
        if form.is_valid() and formset.is_valid():
            restaurant = form.save(commit=False)
            restaurant.address = address
            restaurant.user = request.user
            restaurant.save()
            for forms in formset.cleaned_data:
                if forms:
                    # image file
                    image = forms["image"]
                    print(forms)
                    print(forms["image"])
                    # review, image file save
                    photo = RestaurantImages(restaurant=restaurant, image=image)
                    print(photo)
                    photo.save()
            messages.success(request, "글 작성이 완료되었습니다.")
            return redirect("restaurants:main")
        else:
            print(form.errors, formset.errors)
    else:
        form = RestaurantForm()
        formset = ImageFormSet(queryset=RestaurantImages.objects.none())
    context = {
        "form": form,
        "formset": formset,
    }
    return render(request, "restaurants/forms.html", context)


@require_http_methods(["GET", "POST"])
def update(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_pk)
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        address = request.POST.get("address")
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.address = address
            restaurant.save()
            return redirect("restaurants:detail", restaurant.pk)
    else:
        form = RestaurantForm(instance=restaurant)
    context = {
        "restaurant": restaurant,
        "form": form,
    }
    return render(request, "restaurants/forms.html", context)


def delete(request, restaurant_pk):
    get_object_or_404(Restaurants, pk=restaurant_pk).delete()
    return redirect("restaurants:main")


@login_required
def like(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurants, pk=restaurant_pk)
    if restaurant.like_users.filter(pk=request.user.pk).exists():
        restaurant.like_users.remove(request.user)
        is_like = False
    else:
        restaurant.like_users.add(request.user)
        is_like = True
    context = {
        "isLiked": is_like,
        "likeCount": restaurant.like_users.count(),
    }
    return JsonResponse(context)


def search(request):
    s = Search.objects.filter().order_by("count")[:3]
    if request.method == "GET":
        content_list = Restaurants.objects.all()
        search = request.GET.get("search", "")

        if len(search) >= 0:
            if Search.objects.filter(keyword=search).exists():
                search_keyword = Search.objects.get(keyword=search)
                search_keyword.count += 1
                search_keyword.save()
            else:
                Search.objects.create(keyword=search, count=1)

        if search:
            search_lists = content_list.filter(
                Q(restaurant_name__icontains=search)
                | Q(menu__icontains=search)
                | Q(category__icontains=search)
            )
            context = {
                "search_lists": search_lists,
                "s": s,
            }
            return render(request, "restaurants/search.html", context)
