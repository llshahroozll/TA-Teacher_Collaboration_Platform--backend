from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Course
from rest_framework import status
from .serializers import (
    CourseSerializer, 
    CourseMembersSerializer, 
    UpdateCourseSerializer, 
    CourseTitleSerializer 
)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseTitleSerializer(courses, many=True)
    return Response(serializer.data)


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
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, pk):

    course = check_course_permission(request, pk)
    
    if course is None:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)

 
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
def course_setting(request, pk):
    profile = request.user.profile

    if profile.teacher_tag:
        if profile.course_set.filter(id=pk).exists():
            course = profile.course_set.get(id=pk)
        else:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

    
    if request.method == 'GET':
        serializer = UpdateCourseSerializer(course, many=False)
        return Response(serializer.data)
    
    if request.method == 'POST':
        course.class_time = request.data['class_time']
        course.class_location = request.data['class_location']
        course.group_capacity = request.data['group_capacity']
        course.projects_phase = request.data['projects_phase']
        course.save()
        serializer = UpdateCourseSerializer(course, many=False)
        return Response(serializer.data) 
