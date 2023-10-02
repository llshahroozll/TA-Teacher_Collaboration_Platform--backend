from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course, Project, Schedule, Round
from datetime import datetime, date, time, timedelta


@receiver(post_save, sender=Course)
def create_project(sender, instance, created, **kwargs):
    if created:
        course = instance
        project = Project.objects.create(
            name = str.format("پروژه درس %s" %(course.name)),
            description = "توضیحات پروژه"
        )
        
        course.project = project
        course.save()

