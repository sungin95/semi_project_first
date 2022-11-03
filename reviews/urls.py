from django.urls import path
from . import views


app_name = "reviews"

urlpatterns = [
    path("<int:restaurant_pk>/create/", views.create, name="create"),
    path("<int:review_pk>/<int:restaurant_pk>/detail/", views.detail, name="detail"),
    path("<int:review_pk>/<int:restaurant_pk>/update/", views.update, name="update"),
    path("<int:review_pk>/<int:restaurant_pk>/delete/", views.delete, name="delete"),
    path("<int:review_pk>/like/", views.like, name="like"),
    path("<int:review_pk>/comments/", views.comments, name="comments"),
    path(
        "<int:reviews_pk>/comments/<int:comment_pk>/update/",
        views.comment_update,
        name="comment_update",
    ),
    path(
        "<int:reviews_pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
]
