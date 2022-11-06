from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProfileCustomUserChangeForm,
)
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    users = get_user_model().objects.all()  # 저장된 모든 User를 가져온다.
    context = {
        "users": users,
    }
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # 회원가입과 동시에 로그인을 시키기 위해
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.user.is_authenticated:  # 로그인이 된 상태에서는 로그인 화면에 들어갈 수 없다.
        return redirect("accounts:index")
    if request.method == "POST":
        form = AuthenticationForm(
            request, data=request.POST
        )  # request가 없어도 잘 돌아가는거 같음 하지만 대부분이 request를 필수적으로 받아 가지고 편의상 넣겠음
        if form.is_valid():
            auth_login(request, form.get_user())  # login을 가져와야 한다.
            return redirect(
                request.GET.get("next") or "accounts:index"
            )  # login_required를 사용하기 위해
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    like_restaurant = user.like_restaurant.all()
    context = {
        "user": user,
        "like_restaurants": like_restaurant,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("accounts:login")


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context=context)


def profile(request):
    if request.method == "POST":
        form = ProfileCustomUserChangeForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = ProfileCustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/profile.html", context=context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


@login_required
def follow(request, user_pk):
    person = get_user_model().objects.get(pk=user_pk)
    if person != request.user:
        if person.followers.filter(pk=request.user.pk).exists():
            # if request.user in person.followers.all():
            person.followers.remove(request.user)
        else:
            person.followers.add(request.user)
    return redirect("accounts:profile", person.username)
