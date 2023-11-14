from time import sleep

from django.db.models import Model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate


class BaseTestCase(APITestCase):
    email = 'user@gmail.com'
    password = 'test1234'

    def setUp(self):
        self.user = User.objects.create(
            email=self.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            role='member',  # Can Be Member or Moderator
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.user.set_password(self.password)
        self.user.save()

        self.client = APIClient()
        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=access_token)

    def tearDown(self):
        self.user.delete()


class UserProfileTestCases(BaseTestCase):
    def test_user_get_profile_list(self):
        response = self.client.get(reverse("users:user-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0],
                         {
                             'id': self.user.pk,
                             'payment_history': [],
                             'email': 'user@gmail.com',
                             'first_name': 'Admin',
                             'last_name': 'Admin',
                             'phone': '12345678',
                             'avatar': None,
                             'role': 'member'
                         }
                         )

    def test_user_retrieve_profile(self):
        response = self.client.get(reverse("users:user-profile", args=[self.user.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.user.pk,
                             'payment_history': [],
                             'email': 'user@gmail.com',
                             'first_name': 'Admin',
                             'last_name': 'Admin',
                             'phone': '12345678',
                             'avatar': None,
                             'role': 'member'
                         }
                         )

    def test_user_update_profile(self):
        response = self.client.patch(reverse("users:user-update", args=[self.user.pk]),
                                     data={
                                         'first_name': 'Admin Update',
                                         'last_name': 'Admin Update'
                                     })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),

                         {
                             'id': self.user.pk,
                             'payment_history': [],
                             'email': 'user@gmail.com',
                             'first_name': 'Admin Update',
                             'last_name': 'Admin Update',
                             'phone': '12345678',
                             'avatar': None,
                             'role': 'member'
                         }
                         )

    def test_user_delete_profile(self):
        response = self.client.delete(reverse("users:user-delete", args=[self.user.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
