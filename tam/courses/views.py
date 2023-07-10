from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
# Create your views here.

def json_ret(courseObj):
    course_data = {'name': courseObj.name,
                   'class_time': courseObj.class_time,
                   'class location': courseObj.class_location,
                   'class exam time': courseObj.exam_time,
                   'class status': courseObj.status,
                   }
    
    response = JsonResponse(course_data)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def courses(request):
    courses = Course.objects.all()
    # return HttpResponse(courses.values)
    # contxt = serializers.serialize("json", courses)
    # data = {'courses': contxt}
    # return JsonResponse(data)
    return render(request, 'courses/courses.html',  {'courses': courses})


def course(request, pk):
    courseObj = Course.objects.get(id=pk)
    return json_ret(courseObj)

    # return render(request, 'courses/course.html', {'course': courseObj})


def createCourse(request):
    form = CourseForm()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
    # contxt = serializers.serialize("json", form)
    # data = {"somemodeljson" : contxt}
    # return JsonResponse(data)
    return render(request, 'courses/course_form.html', {'form': form})


def updateCourse(request, pk):
    CourseObj = Course.objects.get(id=pk)
    form = CourseForm(instance=CourseObj)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=CourseObj)
        if form.is_valid():
            form.save()
            return redirect('courses')
    context = {'form': form}
    return render(request, 'courses/course_form.html', context)


def deleteCourse(request, pk):
    course = Course.objects.get(id=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('courses')

    context = {'object': course}
    return render(request, 'courses/delete_template.html', context)
