
from django.db import connection
from rest_framework import status

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User


class CourseTestCases(APITestCase):
    email = 'test@gmail.com'
    password = 'test1234'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email=cls.email,
            first_name='Admin',
            last_name='Admin',
            phone='12345678',
            role='member',  # Can Be Member or Moderator
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

    def test_course_create(self):
        """ Test For Creating Course Object """
        print(connection.queries)

        response = self.client.post(path='/course/', data={
            'name': 'Test Course',
            'description': 'Test Description',
            'course_owner_id': self.user.id,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_course_list(self):
        """ Test To Get Course Objects List """
        response = self.client.get(path='/course/')

        self.assertEqual(response.status_code, status.HTTP_200_OK, )

        self.assertEqual(response.json(),
                         {
                             'count': 1,
                             'next': None,
                             'previous': None,
                             'results': [
                                 {'id': 1,
                                  'name': 'Test Course',
                                  'lesson_list': [],
                                  'lesson_count': 0,
                                  'description': 'Test Description',
                                  'course_owner': 'test@gmail.com'}
                             ]
                         }
                         )

    def test_get_course(self):
        """ Test For Getting Course Object """
        response = self.client.get('/course/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': 1,
                          'name': 'Test Course',
                          'lesson_list': [],
                          'lesson_count': 0,
                          'description': 'Test Description',
                          'course_owner': 'test@gmail.com'
                          }
                         )
