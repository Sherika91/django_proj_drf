from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from course.models import Lesson, Course
from course.validators.lessons import OnlyYouTubeUrlValidator


class LessonListSerializer(serializers.ModelSerializer):
    """ Lesson serializer """
    course = SlugRelatedField(slug_field="name", queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [OnlyYouTubeUrlValidator(field='video')]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
