from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

# Create your views here.


def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review_form.save()
            return redirect("reviews:create")  # ! 여기 수정 필요!!!!!!
    else:
        review_form = ReviewForm()

    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/create.html", context)


def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("reviews:create")  # ! 여기 수정 필요!!!!!!
    else:
        review_form = ReviewForm(instance=review)

    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/create.html", context)


def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    context = {
        "review": review,
    }
    return render(request, "restaurants/detail.html", context)  # ! 여기 수정 필요!!!!!!
