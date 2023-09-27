from rest_framework import serializers
from .models import Course, Group, Project, UploadProject, Round, Schedule
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

class GroupTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'id']


class UpdateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description']
        
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['created', 'project_uploaded_files_zip']


class ProjectZipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_uploaded_files_zip']


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
        
        
class RoundSerializer(serializers.ModelSerializer):
    groups = GroupTitleSerializer(many=True)
    class Meta:
        model = Round
        exclude = ['created']


class GetStudentRoundSerilaizer(serializers.ModelSerializer):
    round_capacity = serializers.SerializerMethodField('get_round_capacity')
    selected = serializers.SerializerMethodField('check_selected')

    class Meta:
        model = Round 
        fields = ['round_name', 'round_capacity', 'selected', 'id', 'start_time', 'finish_time' ]

    def get_round_capacity(self, round):
        number_of_recipints = self.context.get("number_of_recipints")
        number_of_group_in_round = round.groups.all().count()
        round_capacity = number_of_recipints - number_of_group_in_round
        return round_capacity
    
    
    def check_selected(self, round):
        group_id = self.context.get("group_id")
        if round.groups.filter(id=group_id):
            return True
        else:
            return False
        
       