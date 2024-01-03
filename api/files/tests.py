from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import UploadedFile


class GeneralTestCase(APITestCase):
    def setUp(self):
        """
        Setup method to create required objects before running tests.
        """
        self.client = APIClient()
        self.testuser = get_user_model().objects.create_user(
            username="user",
            email="testuser@example.com",
            password="secure#pa$$word_"
        )

        self.valid_uploaded_file = UploadedFile.objects.create(
            user=self.testuser,
            file='https://res.cloudinary.com/dj5u8jfst/image/upload/v1704235061/media/file_chunks/2024/1/1/tuov4goy0wyqcwahbo4k.png',
            name='Test File',
            type='png',
            size='1024',
            uploaded_at='2023-04-27 08:00:00',
        )

        self.invalid_uploaded_file = UploadedFile.objects.create(
            user=self.testuser,
            file='https://res.cloudinary.com/example/image/upload/v1704235061/media/2024/1/1/toler.txt',
            name='Test File',
            type='txt',
            size='1024',
            uploaded_at='2023-04-27 08:00:00',
        )

        self.client.force_authenticate(user=self.testuser)


class UploadedFileModelTest(GeneralTestCase):
    """
    Test cases for the UploadedFile model.
    """

    def test_file_creation(self):
        """
        Test if a file can be created and its string representation is correct.
        """
        uploaded_file = UploadedFile.objects.create(
            user=self.testuser,
            file='https://example.com/file.txt',
            name='Test File',
            type='txt',
            size='1024',
            uploaded_at='2023-04-27 08:00:00',
        )

        self.assertEqual(str(uploaded_file), 'Test File')
        self.assertEqual(uploaded_file.type, 'txt')


class TestChunkCreateView(GeneralTestCase):
    def test_valid_file_upload(self):
        endpoint = reverse('chunks-create')
        data = {
            "uploaded_file_id": self.valid_uploaded_file.id,
            "num_chunks": 3,
        }
        response = self.client.post(endpoint, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_file_upload(self):
        endpoint = reverse('chunks-create')
        data = {
            "uploaded_file_id": self.invalid_uploaded_file.id,
            "num_chunks": 3,
        }
        response = self.client.post(endpoint, data=data)
        print(response.content, 'hiiiiiiii')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class TestChunkListView(GeneralTestCase):
#     def test_chunk_list_view(self):
#         self.client.force_authenticate(user=self.testuser)

#         endpoint = reverse('chunks-list', kwargs={"file_id": 1})
#         response = self.client.get(endpoint)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), get_user_model().objects.count())
