from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .form import ProfileForm
from .serializers import ProfileSerializer
from courses.serializers import CourseTitleSerializer
# Create your views here.


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getProfiles(request):
#     profiles = Profile.objects.all()
#     serializer = ProfileSerializer(profiles, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    profile = request.user.profile
    profile_serializer = ProfileSerializer(profile, many=False)
    
    if profile.teacher_tag : 
        teacher_courses = profile.course_set.all()
        teacher_courses_serializer = CourseTitleSerializer(teacher_courses, many=True)
        
        return Response({"profile": profile_serializer.data,
                        "teacher_courses": teacher_courses_serializer.data,
                        })
        
    else:
        student_courses = profile.student_courses.all()
        assistant_courses = profile.assistant_courses.all()
        
        student_course_serializer = CourseTitleSerializer(student_courses, many=True)
        assistant_courses_serializer = CourseTitleSerializer(assistant_courses, many=True)
        
        
        return Response({"profile": profile_serializer.data,
                        "student_courses": student_course_serializer.data,
                        "assistant_courses": assistant_courses_serializer.data,
                        })



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile = request.user.profile

    if request.method == 'GET':
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    if request.method == 'POST':
        profile.name = request.data['name']
        profile.email = request.data['email']
        profile.profile_image = request.data['profile_image']
        profile.social_github = request.data['social_github']
        profile.social_linkedin = request.data['social_linkedin']
        profile.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)
        
