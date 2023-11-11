from time import sleep

from django.db.models import Model
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate


class UserProfileTestCases(APITestCase):
    email = 'user@gmail.com'
    password = 'password'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email=cls.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            role='moderator',  # Can Be Member or Moderator
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        cls.user.set_password(cls.password)
        cls.user.save()

    def setUp(self):
        self.client = APIClient()
        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=access_token)

    def test_user_get_profile_list(self):
        response = self.client.get('/users/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()[0],
                         {
                             'id': 1,
                             'payment_history': [],
                             'email': 'user@gmail.com',
                             'first_name': 'Admin',
                             'last_name': 'Admin',
                             'phone': '12345678',
                             'avatar': None,
                             'role': 'moderator'
                         }
                         )

    def test_user_retrieve_profile(self):
        response = self.client.get('/users/profile/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'payment_history': [],
                             'email': 'user@gmail.com',
                             'first_name': 'Admin',
                             'last_name': 'Admin',
                             'phone': '12345678',
                             'avatar': None,
                             'role': 'moderator'
                         }
                         )

    def test_user_update_profile(self):
        response = self.client.patch('/users/profile/1/update/',
                                     data={
                                         'first_name': 'AdminUpdate',
                                         'last_name': 'AdminUpdate'
                                     })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'id': 1,
                          'payment_history': [],
                          'email': 'user@gmail.com',
                          'first_name': 'AdminUpdate',
                          'last_name': 'AdminUpdate',
                          'phone': '12345678',
                          'avatar': None,
                          'role': 'moderator'
                          }
                         )

    def test_user_delete_profile(self):
        response = self.client.delete('/users/profile/1/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
