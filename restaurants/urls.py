from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.main, name='main'),
    path('menu/', views.menu, name='menu'),
    path('create/', views.create, name='create'),
    path('detail/<int:restaurant_pk>/', views.detail, name='detail'),
    path('update/<int:restaurant_pk>/', views.update, name='update'),
]