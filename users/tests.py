from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from rest_framework.test import APITestCase, APIClient


class UserProfileListTestCase(APITestCase):
    email = 'user@gmail.com'
    password = 'password'

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email=self.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            role='moderator',  # Can Be Member or Moderator
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.user.set_password(self.password)
        self.user.save()

        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_user_get_profile_list(self):
        response = self.client.get('/users/profile/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()[0],

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


class UserProfileRetrieveTestCase(APITestCase):
    email = 'user@gmail.com'
    password = 'password'

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email=self.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            role='moderator',  # Can Be Member or Moderator
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.user.set_password(self.password)
        self.user.save()

        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_user_retrieve_profile(self):
        response = self.client.get('/users/profile/1/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),

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


class UserProfileUpdateTestCase(APITestCase):
    email = 'user@gmail.com'
    password = 'password'

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email=self.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            role='moderator',  # Can Be Member or Moderator
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.user.set_password(self.password)
        self.user.save()

        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_user_update_profile(self):
        response = self.client.put('/users/profile/1/update/',
                                   data={
                                       'first_name': 'AdminUpdate',
                                       'last_name': 'AdminUpdate'
                                   })
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 1,
             'payment_history': [],
             'email': 'user@gmail.com',
             'first_name': 'AdminUpdate',
             'last_name': 'AdminUpdate',
             'phone': '12345678',
             'avatar': None,
             'role': 'moderator'}

        )


class UserAuthTestCase(APITestCase):
    email = 'test@gmail.com'
    password = 'testpassword'

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email=self.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.user.set_password(self.password)
        self.user.save()

    def test_successful_token_obtain_pair_gives_200(self):
        access_token = AccessToken.for_user(self.user)
        access_token = str(access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(
            '/users/api/token/',
            {
                'email': self.email,
                'password': self.password
            },

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_successful_token_refresh_gives_200(self):
        access_token = RefreshToken.for_user(self.user)
        access_token = str(access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.post(
            '/users/api/token/refresh/',
            {
                'refresh': access_token,
            },

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
