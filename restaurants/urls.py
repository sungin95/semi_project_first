from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('create/', views.create, name='create'),
    path('<int:restaurant_pk>/detail/', views.detail, name='detail'),
    path('<int:restaurant_pk>/update/', views.update, name='update'),
    path('<int:restaurant_pk>/delete/', views.delete, name='delete'),
]