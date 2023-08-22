from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.get_courses,),
    path('course/<str:pk>/', views.get_course),
    path('course/<str:pk>/members', views.get_course_members),
    path('course/<str:pk>/setting/', views.course_setting),
    path('course/<str:pk>/check-assistant/', views.course_check_assistant),
    path('course/<str:pk>/add-assistant/', views.course_add_assistant),
    path('course/<str:pk>/remove-assistant/', views.course_remove_assistant),
]
