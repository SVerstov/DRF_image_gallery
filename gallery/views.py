from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from gallery.models import GalleryImages
from gallery.permissions import IsOwnerOrReadOnly
from gallery.serializers import GallerySerializer


# Create your views here.
class AllGalleryApiList(generics.ListCreateAPIView):
    queryset = GalleryImages.objects.all()
    serializer_class = GallerySerializer


class UserGalleryApiList(generics.ListCreateAPIView):
    serializer_class = GallerySerializer

    def get_queryset(self):
        return GalleryImages.objects.filter(owner_id__exact=self.kwargs['user_id'])


class DetailGalleryApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryImages.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return GalleryImages.objects.filter(owner_id__exact=self.kwargs['user_id'])
