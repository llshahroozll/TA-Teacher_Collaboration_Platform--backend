from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance        
        profile = Profile.objects.create(
            user = user,
            name = user.username,
            email = user.email,
            id = user.username,  
        )
    # else:
    #     user = instance
    #     profile = Profile.objects.get(user=user)
    #     if user.first_name != "" or user.last_name != "" :
    #         name = format("%s %s" %(user.first_name, user.last_name))
    #     else:
    #         name = user.username 
        
    #     profile.name = name
    #     profile.email = user.email
    #     profile.save()
        

@receiver(post_save, sender=Profile)
def update_user(sender, instance, **kwargs):
    profile = instance 
    user = profile.user
    user.email = profile.email
    user.save()




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="TAM"),
        # message:
        email_plaintext_message,
        # from:
        "shahroozakbaripoor@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()