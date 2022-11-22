from rest_framework import serializers
from .models import GalleryImages


class GallerySerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GalleryImages
        fields = '__all__'
