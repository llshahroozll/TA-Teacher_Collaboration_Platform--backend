from rest_framework import serializers
from .models import Course
from users.serializers import ProfileSerializer, ProfileTitleSerializer


class CourseTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'id']
        
        
class CourseSerializer(serializers.ModelSerializer):
    owner = ProfileTitleSerializer(many=False)
    assistant_profiles = ProfileTitleSerializer(many=True)
    student_profiles = ProfileTitleSerializer(many=True)
    class Meta:
        model = Course
        exclude = ['created']


