# Generated by Django 4.2.3 on 2023-07-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_nationalid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default_profile', upload_to='images/profiles'),
        ),
    ]
