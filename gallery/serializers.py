from rest_framework import serializers
from .models import GalleryImages


class GallerySerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # owner = serializers.CreateOnlyDefault(default=serializers.CurrentUserDefault())
    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImages
        fields = ('__all__')

    def get_owner_id(self, obj):
        return obj.owner.pk
