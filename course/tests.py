from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework_simplejwt.settings import api_settings

from course.models import Course, Lesson
from users.models import User


class TestCourse(APITestCase):

    def SetUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@gmail.com', set_password='testpassword')

        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            course_owner=self.user,
        )

    def test_get_course_list(self):
        """ Test To Get Course Objects List """
        response = self.client.get(
            path='/course/',

        )
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


class TestLessons(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@gmail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            course_owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            video='https://www.youtube.com'

        )

    def test_get_lessons_list(self):
        response = self.client.get(
            reverse='/lesson/'

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

