from django.db import models
import uuid

# Create your models here.


class Course(models.Model):
    # teacher = models.ForeignKey(
    #     Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    class_time = models.DateTimeField(blank=True, null=True)
    class_location = models.CharField(max_length=200, blank=True, null=True)
    exam_time = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid1,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return self.name
