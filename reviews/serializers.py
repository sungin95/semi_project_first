from rest_framework import serializers
from .models import Review, ReviewImages


class ReviewImagesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ReviewImages
        fields = ["image"]


class ReviewSerializer(serializers.ModelSerializer):
    images = ReviewImagesSerializer(many=True, read_only=True)

    def get_images(self, object):
        image = object.reviewimages_set.all()
        return ReviewImagesSerializer(review=image, many=True).data

    class Meta:
        model = Review
        fields = ["content", "image"]

    def create(self, validated_data):
        images_data = self.context["request"].FILES
        review = Review.objects.create(**validated_data)
        for image_data in images_data.getlist("image"):
            ReviewImages.objects.create(review=review, image=image_data)
        return review
