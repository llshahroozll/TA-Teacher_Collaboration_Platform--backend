from django.db import models
from users.models import Profile
import uuid
import os

class Project(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    project_file = models.FileField(default=None, upload_to='projects/course_projects/', blank=True, null=True)
    status = models.BooleanField(default=False)
    project_uploaded_files_zip = models.FileField(default=None, upload_to='projects/archives/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        return self.name
    
    

class Course(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    assistant_profiles = models.ManyToManyField(Profile, blank=True, related_name="assistant_courses")
    student_profiles = models.ManyToManyField(Profile, blank=True, related_name="student_courses")
    project = models.OneToOneField(Project, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    class_time = models.CharField(max_length=300, blank=True, null=True)
    class_location = models.CharField(max_length=200, blank=True, null=True)
    exam_time = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=True)
    group_capacity = models.IntegerField(default=3)
    created = models.DateTimeField(auto_now_add=True)
    id = models.IntegerField(primary_key=True, unique=True)

    def __str__(self):
        return self.name



class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(Profile, blank=True, related_name="members")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    class Meta:
        unique_together = [['course', 'creator'] ]
        
    def __str__(self):
        return self.name + " - " + self.creator.name
    
    



def get_upload_path(instance, filename):
    return os.path.join("projects/student_projects/%s/" %(instance), filename)

class UploadProject(models.Model):
    
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    def __str__(self):
        return self.group.course.name



class Round(models.Model):
    round_name = models.CharField(max_length=250, null=True, blank=True)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    groups = models.ManyToManyField(Group, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.round_name    
    


class Schedule(models.Model):
    PERIODS = (
        (5, '5 minutes'),
        (10, '10 minutes'),
        (15, '15 minutes'),
        (20, '20 minutes'),
        (30, '30 minutes'),
    )
    project = models.OneToOneField(Project, null=True, blank=True, on_delete=models.CASCADE)
    rounds = models.ManyToManyField(Round, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    finish_time = models.TimeField()
    period = models.IntegerField(choices=PERIODS)
    number_of_recipints = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    def __str__(self):
        return str.format("%s > %s" %(self.project.name, self.date))