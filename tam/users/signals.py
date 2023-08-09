from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance        
        profile = Profile.objects.create(
            user = user,
            name = user.username,
            email = user.email,  
        )
    else:
        user = instance
        profile = Profile.objects.get(user=user)
        if user.first_name != "" or user.last_name != "" :
            name = format("%s %s" %(user.first_name, user.last_name))
        else:
            name = user.username 
        
        profile.name = name
        profile.email = user.email
        profile.save()
        