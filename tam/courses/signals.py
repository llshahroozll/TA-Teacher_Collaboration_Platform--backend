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






@receiver(post_save, sender=Schedule)
def create_rounds(sender, instance, created, **kwargs):
    if created:
        schedule = instance
        
        schedule_start_time = datetime.combine(date.min, schedule.start_time)
        schedule_finish_time = datetime.combine(date.min, schedule.finish_time)
        schedule_period = schedule.period

        round_number = 1

        while(schedule_start_time + timedelta(minutes=schedule_period) <= schedule_finish_time):
            
            schedule_next_start_time = schedule_start_time + timedelta(minutes=schedule_period)

            round = Round.objects.create(
                round_name = str.format("بازه %i" %round_number),
                start_time = schedule_start_time,
                finish_time = schedule_next_start_time,
            )
            
            schedule.rounds.add(round)
            schedule.save()

            schedule_start_time = schedule_next_start_time
            round_number += 1