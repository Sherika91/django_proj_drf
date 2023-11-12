from rest_framework import status

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from course.models import Course, Lesson
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

        cls.course = Course.objects.create(
            name='Test Course1',
            description='Test Description1',
            course_owner=cls.user,
        )

    def setUp(self):
        self.client = APIClient()
        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=access_token)

    def test_course_create(self):
        """ Test For Creating Course Object """
        response = self.client.post(path='/course/', data={
            'name': 'Test Course',
            'description': 'Test Description',
            'course_owner': self.user.id,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'id': 2,
                             'lesson_list': [],
                             'lesson_count': 0,
                             'name': 'Test Course',
                             'preview': None,
                             'description': 'Test Description',
                             'course_owner': 1
                         }
                         )

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
                                  'lesson_list': [],
                                  'lesson_count': 0,
                                  'name': 'Test Course1',
                                  'preview': None,
                                  'description': 'Test Description1',
                                  'course_owner': 1}
                             ]
                         }
                         )

    def test_get_course(self):
        """ Test For Getting Course Object """
        response = self.client.get('/course/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'lesson_list': [],
                             'lesson_count': 0,
                             'name': 'Test Course1',
                             'preview': None,
                             'description': 'Test Description1',
                             'course_owner': 1
                         }
                         )

    def test_update_course(self):
        """ Test For Updating Course Object """
        response = self.client.patch('/course/1/', data={
            'name': 'Test Course1 Update',
            'description': 'Test Description1 Update',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'lesson_list': [],
                             'lesson_count': 0,
                             'name': 'Test Course1 Update',
                             'preview': None,
                             'description': 'Test Description1 Update',
                             'course_owner': 1
                         }
                         )

    def test_delete_course(self):
        """ Test For Deleting Course Object """
        response = self.client.delete('/course/1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonTestCases(APITestCase):
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

        cls.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            course_owner=cls.user,
        )

        cls.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            lesson_owner=cls.user,
            course=cls.course,
        )

    def setUp(self):
        self.client = APIClient()
        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=access_token)

    def test_lesson_create(self):
        response = self.client.post(path='/lesson/create/', data={
            'name': 'Test Lesson1',
            'description': 'Test Description1',
            'lesson_owner': self.user.id,
            'course': self.course.id,
        }
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'id': 2,
                             'name': 'Test Lesson1',
                             'description': 'Test Description1',
                             'preview': None,
                             'video': None, 'course': 1,
                             'lesson_owner': 1
                         }
                         )

    def test_lesson_get_list(self):
        response = self.client.get(path='/lesson/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'id': 1,
                 'course': 'Test Course',
                 'name': 'Test Lesson',
                 'description': 'Test Description',
                 'preview': None,
                 'video': None,
                 'lesson_owner': 1
                 }
            ]
        }
                         )

    def test_get_lesson(self):
        response = self.client.get(path='/lesson/1/detail/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'name': 'Test Lesson',
                             'description': 'Test Description',
                             'preview': None,
                             'video': None,
                             'course': 1,
                             'lesson_owner': 1
                         }
                         )

    def test_lesson_update(self):
        response = self.client.patch(path='/lesson/1/update/', data={
            'name': 'Test Lesson Update',
            'description': 'Test Description Update',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'name': 'Test Lesson Update',
                             'description': 'Test Description Update',
                             'preview': None,
                             'video': None,
                             'course': 1,
                             'lesson_owner': 1
                         }
                         )

    def test_lesson_delete(self):
        response = self.client.delete(path='/lesson/1/delete/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCases(APITestCase):
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

        cls.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            course_owner=cls.user,
        )

    def setUp(self):
        self.client = APIClient()
        # Get Access Token For Current User (Moderator)
        access_token = AccessToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=access_token)

    def test_subscription_create(self):
        response = self.client.post(path='/course/subscribe/', data={
            'course': self.course.id,
            'user': self.user.id,
        }
                                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'course': 1,
                             'user': 1,
                         }
                         )

    def test_unsubscribe(self):
        response = self.client.delete(path='/course/unsubscribe/', data={
            'course': self.course.id,
            'user': self.user.id,
        }
                                    )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
