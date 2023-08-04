from rest_framework import serializers
from .models import Course
from users.serializers import ProfileSerializer, ProfileTitleSerializer


class CourseTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'id']
        
        
class CourseSerializer(serializers.ModelSerializer):
    owner = ProfileTitleSerializer(many=False)
    assistantProfiles = ProfileTitleSerializer(many=True)
    studentProfiles = ProfileTitleSerializer(many=True)
    class Meta:
        model = Course
        exclude = ['created']

