from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from course.paginators.lessons import LessonPaginator
from course.permissions.lessons_permissions import IsModerator, IsOwner, IsNotModerator
from course.serializers.lessons import LessonSerializer, LessonListSerializer
from course.models import Lesson


# LESSON CRUD VIEWS USING GENERICS APIVIEW
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all().order_by('-id')
    permission_classes = [IsOwner | IsModerator]
    pagination_class = LessonPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsNotModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
