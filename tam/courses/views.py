from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CourseSerializer, CourseMembersSerializer
from rest_framework import status

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getCourses(request):
#     courses = Course.objects.all()
#     serializer = CourseTitleSerializer(courses, many=True)
#     return Response(serializer.data)


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


# def createCourse(request):
#     form = CourseForm()

#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('courses')
#     return render(request, 'courses/course_form.html', {'form': form})


# def updateCourse(request, pk):
#     CourseObj = Course.objects.get(id=pk)
#     form = CourseForm(instance=CourseObj)

#     if request.method == 'POST':
#         form = CourseForm(request.POST, instance=CourseObj)
#         if form.is_valid():
#             form.save()
#             return redirect('courses')
#     context = {'form': form}
#     return render(request, 'courses/course_form.html', context)


# def deleteCourse(request, pk):
#     course = Course.objects.get(id=pk)

#     if request.method == 'POST':
#         course.delete()
#         return redirect('courses')

#     context = {'object': course}
#     return render(request, 'courses/delete_template.html', context)
