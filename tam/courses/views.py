from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def courses(request):
    return HttpResponse('courses page')


def course(request):
    return HttpResponse('single course page')
