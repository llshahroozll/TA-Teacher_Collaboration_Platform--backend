# Generated by Django 4.2.3 on 2023-07-31 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_profile_image'),
        ('courses', '0006_rename_courses_course_profiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='profiles',
        ),
        migrations.AddField(
            model_name='course',
            name='studentProfiles',
            field=models.ManyToManyField(blank=True, related_name='studentCourses', to='users.profile'),
        ),
        migrations.AddField(
            model_name='course',
            name='taProfiles',
            field=models.ManyToManyField(blank=True, related_name='taCourses', to='users.profile'),
        ),
    ]
