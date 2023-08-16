from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=400, blank=True, null=True)
    bio = models.CharField(default="سلام، من یک کاربر سامانه تام هستم",max_length=400, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_image = models.ImageField(
        default='images/profiles/default_profile.png', upload_to='images/profiles/')
    student_tag = models.BooleanField(default=False)
    teacher_tag = models.BooleanField(default=False)
    assistant_tag = models.BooleanField(default=False)
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return str(self.name)
