from pathlib import Path

from django.conf import settings
from django.test import TestCase, Client
from PIL import Image

from gallery.models import GalleryImages
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist

client = Client()


class GalleryImagesTest(TestCase):
    test_username = 'test_user'
    test_image = 'test_image.png'
    test_password = 'qwerty123'

    """ Test module for GalleryImages model """

    def get_test_user(self):
        try:
            user = User.objects.get(username=self.test_username)
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username=self.test_username,
                password=self.test_password,
            )
        return user

    @staticmethod
    def create_test_image(path_to_test_image):
        open(path_to_test_image, 'w').close()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(path_to_test_image, 'png')

    def get_test_img_path(self):
        Path(settings.MEDIA_ROOT, self.test_username).mkdir(parents=True, exist_ok=True)
        path_to_test_image = Path(settings.MEDIA_ROOT, self.test_image)
        return path_to_test_image

    def setUp(self):
        path_to_test_image = self.get_test_img_path()
        self.create_test_image(path_to_test_image)

        GalleryImages.objects.create(
            owner=self.get_test_user(),
            image=str(path_to_test_image)
        )

    def test_image_cleanup(self):
        self.assertTrue(self.get_test_img_path().exists())
        GalleryImages.objects.filter(owner=self.get_test_user()).delete()
        self.assertFalse(self.get_test_img_path().exists())


