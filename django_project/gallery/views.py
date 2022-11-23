from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from gallery.models import GalleryImages
from gallery.permissions import IsOwnerOrReadOnly, IsAdminUserOrCantDestroy
from gallery.serializers import GallerySerializer


# Create your views here.
class AllGalleryApiList(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = GalleryImages.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (IsAdminUserOrCantDestroy, IsAuthenticatedOrReadOnly)

    def destroy(self, request, *args, **kwargs):
        GalleryImages.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetQuerysetMixin:
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        if not user_id:
            user_id = self.request.user.id
        return GalleryImages.objects.filter(owner_id__exact=user_id)


class UserGalleryApiList(GetQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = GallerySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class DetailGalleryApiView(GetQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = GalleryImages.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (IsOwnerOrReadOnly | IsAdminUser,)
