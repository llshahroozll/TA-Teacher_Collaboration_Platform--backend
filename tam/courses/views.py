from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CourseTitleSerializer


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getCourses(request):
#     courses = Course.objects.all()
#     serializer = CourseTitleSerializer(courses, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def course(request, pk):
#     course = Course.objects.get(id=pk)
#     serializer = CourseTitleSerializer(course, many=False)
#     return Response(serializer.data)


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
