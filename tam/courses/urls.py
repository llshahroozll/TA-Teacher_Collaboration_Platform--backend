from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses, name='courses'),
    path('course/<str:pk>', views.course, name='course'),
    path('create-course/', views.createCourse, name='create-course'),
    path('update-course/<str:pk>', views.updateCourse, name='update-course'),
    path('delete-course/<str:pk>', views.deleteCourse, name='delete-course'),
]
