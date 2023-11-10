from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from course.models import Course
from course.paginators.course import CoursePaginator
from course.permissions.course_permissions import IsOwner, IsModerator, IsNotModerator
from course.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('-id')
    pagination_class = CoursePaginator

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ['list']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in permission_classes]
