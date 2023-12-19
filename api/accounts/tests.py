from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class GeneralTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.testuser = get_user_model().objects.create_user(
            username="user",
            email="testuser@example.com",
            password="secure#pa$$word_"
        )
        self.admin_user = get_user_model().objects.create_user(
            username="adminuser",
            email="adminuser@example.com",
            password="secure#pa$$word_",
            is_staff=True,
        )
        self.super_user = get_user_model().objects.create_user(
            username="superuser",
            email="superuser@example.com",
            password="secure#pa$$word_",
            is_superuser=True,
        )
        self.super_admin_user = get_user_model().objects.create_user(
            username="superadminuser",
            email="superadminuser@example.com",
            password="secure#pa$$word_",
            is_staff=True,
            is_superuser=True,
        )


class TestUserListView(GeneralTestCase):
    """
    Test cases for the user list view
    """

    def test_super_and_admin_user_access(self):
        """
        Test the user list view.

        Ensures that the 'users-list' endpoint returns a 200 status code
        and that the number of users in the response data matches the
        total number of user objects in the database.
        """
        self.client.force_authenticate(user=self.super_admin_user)

        endpoint = reverse('users-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), get_user_model().objects.count())

    def test_other_users_access(self):
        """
        Test API view returns 403 Forbidden if user is not a super user who's an admin.
        """
        other_users = [self.super_user, self.admin_user, self.testuser]

        for user in other_users:
            self.client.force_authenticate(user=user)
            endpoint = reverse('users-list')
            response = self.client.get(endpoint)

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.client.logout()

    def test_unauthenticated_user_access(self):
        """
        Test API view returns 401 Unauthorized if user is not authenticated.
        """
        self.client.logout()
        endpoint = reverse('users-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
