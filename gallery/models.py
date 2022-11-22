from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


def _make_image_path(instance, filename):
    return instance.owner.username + '/' + filename


class GalleryImages(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField('Изображение', upload_to=_make_image_path)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, )


@receiver(pre_delete, sender=GalleryImages)
def delete_image_file(sender, instance, **kwargs):
    instance.image.delete(save=False)
