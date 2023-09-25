from django.contrib import admin
from .models import Course, Group, Project, UploadProject, Schedule
# Register your models here.

admin.site.register(Course)
admin.site.register(Group)
admin.site.register(Project)
admin.site.register(UploadProject)
admin.site.register(Schedule)
