from rest_framework import serializers
from .models import Course
from users.serializers import ProfileSerializer

class CourseSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    class Meta:
        model = Course
        exclude = ['created']