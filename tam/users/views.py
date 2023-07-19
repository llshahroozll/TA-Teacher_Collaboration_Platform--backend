from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse
from .models import Profile
from django.contrib import messages
# Create your views here.


def loginUser(request):
    print("our request")
    print(request)
    return HttpResponse()
    # response = JsonResponse({'request': request}, safe=False)
    # response['Access-Control-Allow-Origin'] = '*'
    # return response
    # return HttpResponse(request)
    # print(request)
    # return render(request, 'users/loginPage.html')


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'users/profile.html', context)
