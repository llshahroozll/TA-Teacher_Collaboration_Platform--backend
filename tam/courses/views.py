from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Course, Group, Project, UploadProject
from users.models import Profile
from users.serializers import ProfileTitleSerializer
from rest_framework import status
from .serializers import (
    CourseSerializer, 
    CourseMembersSerializer, 
    UpdateCourseSerializer, 
    CourseTitleSerializer,
    CheckCourseGroupSerilaizer,
    GroupSerializer,
    UpdateGroupSerializer,
    ProjectSerializer,
    ProjectZipSerializer,
    GetProjectSerializer,
    UploadProjectTitleSerializer,
    UploadProjectSerializer,

)


############################## other function ###########################################

def check_course_permission(request, pk):
    profile = request.user.profile

    try:
        if profile.student_tag and profile.assistant_tag:
            if profile.assistant_courses.filter(id=pk).exists():
                course = profile.assistant_courses.get(id=pk)

            else:
                course = profile.student_courses.get(id=pk)
                    
        elif profile.student_tag:
            course = profile.student_courses.get(id=pk)
    
        elif profile.assistant_tag:
            course = profile.assistant_courses.get(id=pk)
            
        else:
            course = profile.course_set.get(id =pk)
            
        return course
    
    except :
        return None
    

def check_user_status(request, pk):
    profile = request.user.profile
    try:
        if profile.student_tag and profile.assistant_tag:
            if profile.assistant_courses.filter(id=pk).exists():
                course = profile.assistant_courses.get(id=pk)
                group_status = 2      # 2 means user is assistant
                user_role = "A"
            else:
                course = profile.student_courses.get(id=pk)
                if course.group_set.filter(creator=profile):
                    group_status = 3  # 3 means user is student and has group
                    user_role = "S"
                elif course.group_set.filter(members=profile):
                    group_status = 4  # 4 means user is student and has group
                    user_role = "S"
                else:
                    group_status = 5  # 5 means user is student and has not group
                    user_role = "S"
                        
        elif profile.student_tag:
            course = profile.student_courses.get(id=pk)
            if course.group_set.filter(creator=profile):
                group_status = 3  # 3 means user is student and has group
                user_role = "S"
            elif course.group_set.filter(members=profile):
                group_status = 4  # 4 means user is student and has group
                user_role = "S"
            else:
                group_status = 5  # 5 means user is student and has not group
                user_role = "S"
                  
        elif profile.assistant_tag:
            course = profile.assistant_courses.get(id=pk)
            group_status = 2      # 2 means user is assistant 
            user_role = "A"
            
        else:
            course = profile.course_set.get(id =pk)
            group_status = 1      # 1 means user is teacher
            user_role = "T"
            
        return course, group_status, user_role
    except: 
        return None, 0, ""



def check_teacher_permission(request, pk):
    profile = request.user.profile
    if profile.teacher_tag:
        if profile.course_set.filter(id=pk).exists():
            return profile.course_set.get(id=pk)
        return None
    return None




####################################### views ####################################



@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseTitleSerializer(courses, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, pk):
    
    course, group_status, user_role = check_user_status(request, pk)
    
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    #check project status 
    project_status = False
    if course.project is not None:
        if course.project.status:
            project_status = True

            
    serializer = CourseSerializer(course, many=False)
    return Response({"course":serializer.data,
                    "group_status": group_status,
                    "project_status": project_status})


 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_members(request, pk):
    
    course = check_course_permission(request, pk)
    
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CourseMembersSerializer(course, many=False)
    return Response(serializer.data)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def update_course(request, pk):
    course = check_teacher_permission(request, pk)
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    
    if request.method == 'GET':
        serializer = UpdateCourseSerializer(course, many=False)
        return Response(serializer.data)
    
    if request.method == 'POST':
        
        course.class_time = request.data['class_time']
        course.class_location = request.data['class_location']
        course.group_capacity = request.data['group_capacity']
        course.save()
        serializer = UpdateCourseSerializer(course, many=False)
        return Response(serializer.data) 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_check_assistant(request, pk):
    
    course = check_teacher_permission(request, pk)
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        student_id = request.data['student_id']
        
        if course.student_profiles.filter(id=student_id):
            return Response({"error": "This student has this course and could'nt be assistant"}, 
                            status=status.HTTP_406_NOT_ACCEPTABLE)
            
        if course.assistant_profiles.filter(id=student_id):
            return Response({"error": "This assistant is exist"}, status=status.HTTP_409_CONFLICT)
        
        try: 
            profile = Profile.objects.get(id=student_id)
            serializer = ProfileTitleSerializer(profile, many=False)
            return Response(serializer.data)
        except:
            return Response({"error": "There is not any student with this id"}, status=status.HTTP_404_NOT_FOUND)

    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_add_assistant(request, pk):
    course = check_teacher_permission(request, pk)
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        student_id = request.data['student_id']
        
        try:
            profile = Profile.objects.get(id=student_id)
            course.assistant_profiles.add(profile)
            profile.assistant_tag = True 
            profile.save()
            return Response({"message":"success"}, status=status.HTTP_200_OK)
        except:
           return Response({"error": "faild"}, status=status.HTTP_410_GONE)
             
             
@api_view(['POST'])
@permission_classes([IsAuthenticated])         
def course_remove_assistant(request, pk):
    course = check_teacher_permission(request, pk)
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        assistant_id = request.data['assistant_id']

        try:
            profile = course.assistant_profiles.get(id=assistant_id)
            course.assistant_profiles.remove(profile)
            
            if profile.assistant_courses.all().count() == 0:
                profile.assistant_tag = False
                profile.save()
                
            return Response({"massage":"success"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "faild"}, status=status.HTTP_410_GONE)
        
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_course_group(request, pk):

    course, group_status, user_role = check_user_status(request, pk)
    
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

    
    return Response({"group_status": group_status})
    
 
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_list(request, pk):
    
    try:
        profile = request.user.profile
        
        if profile.course_set.filter(id=pk):
            course = profile.course_set.get(id =pk)
        else:
            course = profile.assistant_courses.get(id=pk)
            
        group_list = course.group_set.all()
        serializer = GroupSerializer(group_list, many=True)
        return Response(serializer.data) 
            
    except :
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_head_data(request, pk):
    try:
        profile = request.user.profile
        course = profile.student_courses.get(id=pk)
        if not course.group_set.filter(creator=profile) or  not course.group_set.filter(members=profile):
            serializer = CheckCourseGroupSerilaizer(course, many=False)
            return Response(serializer.data)
    except:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_detail(request, pk):
    try:
        profile = request.user.profile
        course = profile.student_courses.get(id=pk)
        if course.group_set.filter(creator=profile):
            group = course.group_set.get(creator=profile)
            group_status = 2
        else:
            group = course.group_set.get(members=profile)
            group_status = 3
        
        course_serializer = CheckCourseGroupSerilaizer(course, many=False)
        group_serializer = GroupSerializer(group, many=False)
        return Response({"group":group_serializer.data,
                         "course": course_serializer.data,
                         "group_status": group_status})
            
    except:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_group(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            
            course, group_status, user_role = check_user_status(request, pk)
            if course is None:
                return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            
            group_id = request.data['id']
            
            if group_status == 1:
                group = course.group_set.get(id=group_id)
                group.delete()
                return Response({"message":"success"}, status=status.HTTP_200_OK)
            else:
                group = profile.group_set.get(id=group_id)
                group.delete()
                return Response({"message":"success"}, status=status.HTTP_200_OK)
                
        except :
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
     
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            course = profile.student_courses.get(id=pk)
            
            if course.group_set.filter(creator = profile) or course.group_set.filter(members = profile):
                return Response({"error": "You already hava a group."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            try:
                Group.objects.create(
                    course = course,
                    creator = profile,
                    name = request.data["name"],
                    description = request.data["description"],
                )
                return Response({"message":"success"}, status=status.HTTP_200_OK)
            
            except:
                return Response({"error": "This name already exist, insert another name for your group"}, status=status.HTTP_409_CONFLICT)
                    
        except :
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_group_member(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            course = profile.student_courses.get(id=pk)
            group = profile.group_set.get(course=course)
            
            student_id = request.data["student_id"]
            
            student_profile = Profile.objects.get(id=student_id)
            
            if not student_profile.student_courses.filter(id=pk):
                return Response({"error": "Student has not this course"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            if course.group_set.filter(creator = student_profile) or course.group_set.filter(members = student_profile):
                return Response({"error": "Student already has a group."}, status=status.HTTP_409_CONFLICT)
    
            serializer = ProfileTitleSerializer(student_profile, many=False)
            return Response(serializer.data)
            
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_group_member(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            course = profile.student_courses.get(id=pk)
            group = profile.group_set.get(course=course)
            group_members_count = ( group.members.all().count() ) + 1

            if course.group_capacity <=  group_members_count:
                return Response({"error":"Your group is full"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            student_id = request.data["student_id"]
            
            student_profile = Profile.objects.get(id=student_id)
            
            if not student_profile.student_courses.filter(id=pk):
                return Response({"error": "Student has not this course"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            if course.group_set.filter(creator = student_profile) or course.group_set.filter(members = student_profile):
                return Response({"error": "Student already has a group."}, status=status.HTTP_409_CONFLICT)
    
            group.members.add(student_profile)
            return Response({"message":"success"}, status=status.HTTP_200_OK)
            
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
              

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_group_member(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            course = profile.student_courses.get(id=pk)
            group = profile.group_set.get(course=course)
            
            student_id = request.data["student_id"]
            
            student_profile = group.members.get(id= student_id)
            group.members.remove(student_profile)
            return Response({"message":"success"}, status=status.HTTP_200_OK)
            
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)



      
        
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def update_group(request, pk):
    try:
        profile = request.user.profile
        course = profile.student_courses.get(id=pk)
        group = profile.group_set.get(course=course)
        
        if request.method == 'GET':
            serializer = UpdateGroupSerializer(group, many=False)
            return Response(serializer.data)
        
        if request.method == 'POST':
            try:    
                group.name = request.data["name"]
                group.description = request.data["description"]
                group.save()
                
                serializer = UpdateGroupSerializer(group, many=False)
                return Response(serializer.data)
            
            except:
                return Response({"error": "This name already exist"}, status=status.HTTP_409_CONFLICT)
            
    except:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_member(request, pk):
    if request.method == "POST":
        try:
            profile = request.user.profile
            
            group_id = request.data["group_id"]
            group = Group.objects.get(id=group_id)
            
            profile = group.members.get(id=profile.id)
            group.members.remove(profile)
            return Response({"message":"success"}, status=status.HTTP_200_OK)
            
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            

################# project section #########################


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def update_project(request, pk):
    
    course = check_teacher_permission(request, pk)
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        project = course.project
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)
        
    if request.method == 'POST':
        project = course.project
    
    try:   
        project.name = request.data["name"]
        project.description = request.data["description"]
        if request.data["project_file"] != "":
            project.project_file = request.data["project_file"]
        project.status = request.data["status"]
        project.save()
        
        serializer = ProjectSerializer(course.project, many=False)
        return Response(serializer.data)
    
    except:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)


#function for check student to has group. it used in these views : get_project, update_project
def check_student_has_group(course, profile):
    if course.group_set.filter(creator=profile):
        group = course.group_set.get(creator=profile)
    elif course.group_set.filter(members=profile):
        group = course.group_set.get(members=profile)
    else:
        group = None

    return group


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, pk):
    if request.method == 'GET':
        try:
            profile = request.user.profile
            course = profile.student_courses.get(id=pk)
            project = course.project
            
            if not project.status:
                return Response({"error":"project has not been defined yet"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            project_serializer = GetProjectSerializer(project, many=False) 
            group = check_student_has_group(course, profile)
            
            if group:
                group_serializer = GroupSerializer(group, many=False)
                group_uploaded_project = group.uploadproject_set.all()
                group_uploaded_project_serializer = UploadProjectSerializer(group_uploaded_project, many=True)
                return Response({"project_detail" : project_serializer.data,
                                 "group_detail" : group_serializer.data,
                                "group_uploaded_project" : group_uploaded_project_serializer.data
                                })
            else:
                return Response({"project_detail" : project_serializer.data})
            
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_project(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            course = profile.student_courses.get(id=pk)
            project = course.project
            
            group = check_student_has_group(course, profile)
            if group is None:
                return Response({"error": "You don't have any group, JOIN A GROUP OR CREATE ONE"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            UploadProject.objects.create(
                sender = profile,
                group = group,
                project = project,
                file = request.data["file"]
            )
            
            return Response({"message":"success"}, status=status.HTTP_200_OK)
                       
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def uploaded_project_list(request, pk):
    
    if request.method == 'GET':
        profile = request.user.profile
        try:    
            if profile.course_set.filter(id=pk):
                course = profile.course_set.get(id =pk)
            else:
                course = profile.assistant_courses.get(id=pk)

            project = course.project
            uploaded_project_list = project.uploadproject_set.all()
            serializer = UploadProjectTitleSerializer(uploaded_project_list, many=True)
            return Response(serializer.data)
                
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_uploaded_project(request, pk):
    if request.method == 'POST':
        profile = request.user.profile
        try:
            if profile.course_set.filter(id=pk):
                course = profile.course_set.get(id =pk)
            else:
                course = profile.assistant_courses.get(id=pk)
            
            project = course.project
    
            upload_project_id = request.data["upload_project_id"]
            
            upload_project = project.uploadproject_set.get(id=upload_project_id)
            serializer = UploadProjectSerializer(upload_project, many=False)
            return Response(serializer.data)
            
        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            

import shutil 
import os
from tam import settings
from wsgiref.util import FileWrapper

import shutil 
import os
from tam import settings

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_project(request, pk):
    if request.method == 'GET':
        try:
            profile = request.user.profile
            if profile.course_set.filter(id=pk):
                course = profile.course_set.get(id =pk)
            else:
                course = profile.assistant_courses.get(id=pk)

            project = course.project
            if not project.uploadproject_set.filter():
                return Response({"message": "there are not any uploaded projects"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            zip_file_name = str.format("پروژه آپلود شده دانشجویان درس %s" %(course.name))
            zip_file_name_with_format = str.format("پروژه آپلود شده دانشجویان درس %s.zip" %(course.name))
            archive_base_dir = os.path.join(settings.MEDIA_ROOT, "projects/student_projects/")
            archive_destination_dir = os.path.join(settings.MEDIA_ROOT, "projects/archives/")
            
            zip_file= shutil.make_archive(base_name=zip_file_name, format='zip', root_dir=archive_base_dir, base_dir=course.name)
            zip_file_path = os.path.join(archive_destination_dir, zip_file_name_with_format)

            if os.path.exists(os.path.join(zip_file_path)):
                os.remove(os.path.join(zip_file_path))

            shutil.move(zip_file  , archive_destination_dir)

            project.project_uploaded_files_zip = zip_file_path
            project.save()
   
            serializer = ProjectZipSerializer(project, many=False)
            return Response(serializer.data)

        except:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
        





