# Generated by Django 4.2.3 on 2023-07-31 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_profile_image'),
        ('courses', '0004_course_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='courses', to='users.profile'),
        ),
    ]
