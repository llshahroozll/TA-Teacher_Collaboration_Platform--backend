# Generated by Django 4.2.3 on 2023-08-05 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_profile_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='nationalID',
            new_name='national_id',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='social_linkedIn',
            new_name='social_linkedin',
        ),
    ]
