import io

from PIL import Image
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from gallery.models import GalleryImages
from django.core.files.uploadedfile import SimpleUploadedFile

client = APIClient()


class GalleryTest(APITestCase):
    admin_name = 'admin'
    username = 'test_gallery'
    password = 'test_password'
    user_auth_token = None
    admin_auth_token = None

    @classmethod
    def setUpTestData(cls):
        """ registration, login and get 2 auth_tokens """
        url = '/auth/users/'
        client.post(url, data={'username': cls.username, 'password': cls.password})
        cls.user_auth_token = cls.login(cls.username, cls.password)

        client.post(url, data={'username': cls.admin_name, 'password': cls.password})
        cls.admin_auth_token = cls.login(cls.admin_name, cls.password)

        admin = User.objects.get(username=cls.admin_name)
        admin.is_staff = True
        admin.save()

        # cls.assertEqual(User.objects.count(), 2)
        # cls.assertTrue(cls.auth_token and cls.admin_auth_token)

        cls.create_image_record(cls, 'img1.png', cls.user_auth_token)
        cls.create_image_record(cls, 'img2.png', cls.admin_auth_token)

    @staticmethod
    def login(username, password):
        url = reverse('login')
        response = client.post(url, data={'username': username, 'password': password})
        return response.data.get('auth_token')

    @staticmethod
    def create_test_image():
        image = io.BytesIO()
        Image.new('RGBA', size=(50, 50), color=(155, 0, 0)).save(image, 'PNG')
        image.seek(0)
        return image.getvalue()

    def create_image_record(cls, img_name, auth_token: str):
        url = reverse('all_gallery')
        client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        imagefile = SimpleUploadedFile(img_name, cls.create_test_image())
        client.post(url, data={'image': imagefile}, format='multipart')

    def test_all_gallary(self):
        response = self.client.get(reverse('all_gallery'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_all(self):
        """ test admin can gelete all gallary"""
        url = reverse('all_gallery')
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_auth_token)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_fail_delete_all(self):
        """ test user can't gelete all gallary"""
        url = reverse('all_gallery')
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_auth_token)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_image(self):
        url = reverse('one_image', args=(1, 1))
        response = client.get(url)
        self.assertEqual(type(response.json()), dict)

    def test_add_to_user_gallery(self):
        url = reverse('user_gallery', '1')
        self.create_image_record('img3.png', self.user_auth_token)
        self.create_image_record('img4.png', self.user_auth_token)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_auth_token)
        response = client.get(url)
        # print(response.data)
        self.assertEqual(len(response.json()), 3)
        # test another url user_gallery/0/
        url = reverse('user_gallery', '0')
        response = client.get(url)
        self.assertEqual(len(response.json()), 3)

    def test_user_delete_img(self):
        url = reverse('one_image', args=(1, 1))
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
