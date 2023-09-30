from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.get_courses,),
    path('course/<str:pk>/', views.get_course),
    path('course/<str:pk>/members/', views.get_course_members),

    path('course/<str:pk>/update-course/', views.update_course),
    path('course/<str:pk>/check-assistant/', views.course_check_assistant),
    path('course/<str:pk>/add-assistant/', views.course_add_assistant),
    path('course/<str:pk>/remove-assistant/', views.course_remove_assistant),

    path('course/<str:pk>/check-group/', views.check_course_group),
    path('course/<str:pk>/group-list/', views.get_group_list),
    path('course/<str:pk>/head-data/', views.get_head_data),
    path('course/<str:pk>/group-detail/', views.get_group_detail),
    path('course/<str:pk>/remove-group/', views.remove_group),
    path('course/<str:pk>/create-group/', views.create_group),
    path('course/<str:pk>/check-group-member/', views.check_group_member),
    path('course/<str:pk>/add-group-member/', views.add_group_member),
    path('course/<str:pk>/remove-group-member/', views.remove_group_member),
    path('course/<str:pk>/update-group/', views.update_group),
    path('course/<str:pk>/leave-member/', views.leave_member),
    
    path('course/<str:pk>/update-project/', views.update_project),
    path('course/<str:pk>/get-project/', views.get_project), 
    path('course/<str:pk>/upload-project/', views.upload_project),
    path('course/<str:pk>/uploaded-project-list/', views.uploaded_project_list),
    path('course/<str:pk>/get-uploaded-project/', views.get_uploaded_project),
    path('course/<str:pk>/get-all-project/', views.get_all_project),
    

    path('course/<str:pk>/schedule/', views.schedule),
    path('course/<str:pk>/create-schedule/', views.create_schedule),
    path('course/<str:pk>/get-manager-round/', views.get_manager_round),
    path('course/<str:pk>/delete-round/', views.delete_round),
    path('course/<str:pk>/get-student-round/', views.get_student_round),
    path('course/<str:pk>/select-round/', views.select_round),
    
]
