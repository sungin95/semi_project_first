from urllib import request
from django.shortcuts import render, redirect
from .models import Review, Comment, ReviewImages
from .forms import CommentForm, ReviewForm, ReviewImageForm
from django.contrib.auth.decorators import login_required
from restaurants.models import Restaurants
from rest_framework.viewsets import ModelViewSet
from .serializers import ReviewSerializer
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.


def create(request, restaurant_pk):
    ImageFormSet = modelformset_factory(ReviewImages, form=ReviewImageForm, extra=5)
    restaurant = Restaurants.objects.get(pk=restaurant_pk)
    grade_ = request.POST.get("grade")
    grade = 0
    if grade_ == "5":
        grade = 5
    elif grade_ == "3":
        grade = 3
    elif grade_ == "1":
        grade = 1
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        formset = ImageFormSet(
            request.POST, request.FILES, queryset=ReviewImages.objects.none()
        )
        if review_form.is_valid() and formset.is_valid():
            review = review_form.save(commit=False)
            review.restaurants = restaurant
            review.user = request.user
            review.grade = grade
            review.save()
            for form in formset.cleaned_data:
                if form:
                    # image file
                    image = form["image"]
                    # review, image file save
                    photo = ReviewImages(review=review, image=image)
                    photo.save()
            # index url 로 요청보냄
            return redirect("restaurants:detail", restaurant.pk)
            # return HttpResponseRedirect("/")
        else:
            print(review_form.errors, formset.errors)
    else:
        review_form = ReviewForm()
        formset = ImageFormSet(queryset=ReviewImages.objects.none())
    context = {
        "name": restaurant.restaurant_name,
        "review_form": review_form,
        "restaurant": restaurant,
        "formset": formset,
    }
    return render(request, "reviews/create.html", context)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


def update(request, restaurant_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    restaurant = Restaurants.objects.get(pk=restaurant_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.restaurants = restaurant
            review.user = request.user
            review.save()
            return redirect("restaurants:detail", restaurant.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/update.html", context)


def detail(request, review_pk, restaurant_pk):
    review = Review.objects.get(pk=review_pk)
    restaurant = Restaurants.objects.get(pk=restaurant_pk)
    context = {
        "review": review,
        "restaurant": restaurant,
    }
    return render(request, "reviews/detail.html", context)  # ! 여기 수정 필요!!!!!!


def delete(request, review_pk, restaurant_pk):
    review = Review.objects.get(pk=review_pk)
    restaurant = Restaurants.objects.get(pk=restaurant_pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
            return redirect("restaurants:detail", restaurant.pk)
    return redirect("reviews:detail", review.pk)


@login_required
def like(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.like.filter(pk=request.user.pk).exists():
        review.like.remove(request.user)
        is_like = False
    else:
        review.like.add(request.user)
        is_like = True
    context = {
        "is_like": is_like,
        "liketCount": review.like.count(),
    }
    return redirect("reviews.detail", review.pk)


def comments(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_review = comment_form.save(commit=False)
            comment_review.review = review
            comment_review.user = request.user
            comment_review.save()
    context = {
        "comment_review_content": comment_review.content,
    }
    return JsonResponse(context)


@login_required
def comment_update(request, review_pk, comment_pk):
    review = Review.objects.get(pk=review_pk)
    comment = Comment.objects.get(pk=comment_pk)

    if request.user != comment.user:
        return redirect("restaurants:detail", review.pk)

    if request.method == "POST":
        update_comment = request.POST.get("update_comment")
        comment.content = update_comment
        comment.review = review
        comment.save()
    return redirect("restaurants:detail", review.pk)


@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user != comment.user:
        return redirect("restaurants:detail", review_pk)
    if request.method == "POST":
        comment.delete()
    return redirect("restaurants:detail", review_pk)
