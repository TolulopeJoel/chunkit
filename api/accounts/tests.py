from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestUserView(APITestCase):
    """
    Test cases for the user list view
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="testpassword2"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_list_view(self):
        """
        Test the user list view.

        Ensures that the 'users-list' endpoint returns a 200 status code
        and that the number of users in the response data matches the
        total number of user objects in the database.
        """
        endpoint = reverse('users-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), get_user_model().objects.count())

    def test_unauthenticated_user_access(self):
        """
        Test API view returns 401 Unauthorized if user is not authenticated.
        """
        self.client.logout()
        endpoint = reverse('users-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
