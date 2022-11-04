from .models import Review, Comment, ReviewImages
from django import forms
from django.utils.translation import gettext_lazy as _


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            # "title",
            "content",
            # "image",
        ]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "주문하신 메뉴는 어떠셨나요? 식당의 분위기와 서비스도 궁금해요!",
                }
            ),
        }
        labels = {
            # "title": "제목",
            "content": "",
            # "image": "",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]


class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImages
        fields = ("image",)
        labels = {
            "image": _("Image"),
        }
