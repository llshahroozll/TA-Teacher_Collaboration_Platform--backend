# Generated by Django 4.2.3 on 2023-08-05 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_profile_image'),
        ('courses', '0008_remove_course_taprofiles_course_assistantprofiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='assistantProfiles',
        ),
        migrations.RemoveField(
            model_name='course',
            name='studentProfiles',
        ),
        migrations.AddField(
            model_name='course',
            name='assistant_profiles',
            field=models.ManyToManyField(blank=True, related_name='assistant_courses', to='users.profile'),
        ),
        migrations.AddField(
            model_name='course',
            name='student_profiles',
            field=models.ManyToManyField(blank=True, related_name='student_courses', to='users.profile'),
        ),
    ]
