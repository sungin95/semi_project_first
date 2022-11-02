from .models import Review, Comment
from django import forms


class ReviewForm(forms.modelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "image",
        ]


class CommentForm(forms.modelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
