from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from .serializers import ProfileSerializer, ChangePasswordSerializer
from courses.serializers import CourseTitleSerializer
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


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
        profile.email = request.data['email']
        profile.bio = request.data['bio']
        if request.data['profile_image'] is not None:
            profile.profile_image = request.data['profile_image']
        profile.social_github = request.data['social_github']
        profile.social_linkedin = request.data['social_linkedin']
        profile.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):            
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    