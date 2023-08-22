from rest_framework import serializers
from .models import Course
from users.serializers import ProfileTitleSerializer


class CourseTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'id']

class UpdateCourseSerializer(serializers.ModelSerializer):
    assistant_profiles = ProfileTitleSerializer(many=True)
    class Meta:
        model= Course
        fields = ['assistant_profiles', 'class_time', 'class_location', 
                  'group_capacity', 'projects_phase']        

class CourseSerializer(serializers.ModelSerializer):
    owner = ProfileTitleSerializer(many=False)
    assistant_profiles = ProfileTitleSerializer(many=True)

    class Meta:
        model = Course
        exclude = ['created', 'student_profiles']


class CourseMembersSerializer(serializers.ModelSerializer):
    owner = ProfileTitleSerializer(many=False)
    assistant_profiles = ProfileTitleSerializer(many=True)
    student_profiles = ProfileTitleSerializer(many=True)
    class Meta:
        model = Course
        fields = ['owner', 'assistant_profiles', 'student_profiles']
