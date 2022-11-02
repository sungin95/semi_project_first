from urllib import request
from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import CommentForm, ReviewForm
from django.contrib.auth.decorators import login_required
from restaurants.models import Restaurants

# Create your views here.


def create(request, restaurant_pk):
    restaurant = Restaurants.objects.get(pk=restaurant_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.restaurants = restaurant
            review.user = request.user
            review.save()
            return redirect("restaurants:detail", restaurant.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/create.html", context)


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
    return render(request, "reviews/create.html", context)


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

    return redirect("restaurants:detail", review.pk)


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
