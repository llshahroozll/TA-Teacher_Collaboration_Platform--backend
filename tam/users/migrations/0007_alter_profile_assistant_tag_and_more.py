# Generated by Django 4.2.3 on 2023-08-08 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_nationalid_profile_national_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='assistant_tag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='student_tag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='teacher_tag',
            field=models.BooleanField(default=False),
        ),
    ]
