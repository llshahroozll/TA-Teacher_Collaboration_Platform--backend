# Generated by Django 4.2.3 on 2023-08-08 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='default_profile.png', upload_to='images/profiles/'),
        ),
    ]
