from django.db import models
from users.models import Profile
import uuid
# Create your models here.


class Course(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    assistant_profiles = models.ManyToManyField(Profile, blank=True, related_name="assistant_courses")
    student_profiles = models.ManyToManyField(Profile, blank=True, related_name="student_courses")
    name = models.CharField(max_length=200)
    class_time = models.CharField(max_length=300, blank=True, null=True)
    class_location = models.CharField(max_length=200, blank=True, null=True)
    exam_time = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField(default=True)
    group_capacity = models.IntegerField(default=3)
    projects_phase = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    id = models.IntegerField(primary_key=True, unique=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    members = models.ManyToManyField(Profile, blank=True, related_name="members")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    class Meta:
        unique_together = [['course', 'creator'] ]
        
    def __str__(self):
        return self.name + " - " + self.creator.name
    
    
