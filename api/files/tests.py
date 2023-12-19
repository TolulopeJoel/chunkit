from django.contrib.auth import get_user_model
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
            file='https://example.com/file.txt',
            name='Test File',
            type='txt',
            size='1024',
            uploaded_at='2023-04-27 08:00:00',
        )

        self.invalid_uploaded_file = UploadedFile.objects.create(
            user=self.testuser,
            file='https://example.com/file.txt',
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
