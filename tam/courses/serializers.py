from rest_framework import serializers
from .models import Course, Group, Project, UploadProject
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
                  'group_capacity']        

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

class CheckCourseGroupSerilaizer(serializers.ModelSerializer):
    owner = ProfileTitleSerializer(many=False)
    class Meta:
        model = Course
        fields = ['owner', 'name', 'id', 'group_capacity']
        
        
class GroupSerializer(serializers.ModelSerializer):
    creator = ProfileTitleSerializer(many=False)
    members = ProfileTitleSerializer(many=True)
    class Meta:
        model = Group
        exclude = ['created']
        
class UpdateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description']
        
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['created']
    
class GetProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_file']
        

class GroupCreatorSerializer(serializers.ModelSerializer):
    creator = ProfileTitleSerializer(many=False)
    class Meta:
        model = Group
        fields = ['id', 'name', 'creator']
        
 
class UploadProjectSerializer(serializers.ModelSerializer):
    sender = ProfileTitleSerializer(many=False)
    group = GroupCreatorSerializer(many=False)
    class Meta:
        model = UploadProject
        fields = '__all__'       
        
        
class UploadProjectTitleSerializer(serializers.ModelSerializer):
    group = GroupCreatorSerializer(many=False)
    class Meta:
        model = UploadProject
        fields = ['group', 'id']
        
        
        
class GetAllUploadProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadProject
        fields = ['file']
        
