from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Course, Project


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