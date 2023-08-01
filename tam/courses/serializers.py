from rest_framework import serializers
from .models import Course
from users.models import Profile
from users.serializers import ProfileSerializer


class CourseTitleSerializer(serializers.ModelSerializer):
    # owner = ProfileSerializer(many=False)
    # taProfiles = ProfileSerializer(many=True)
    # studentProfiles = ProfileSerializer(many=True)
    class Meta:
        model = Course
        fields = ['name', 'id']
        
        

