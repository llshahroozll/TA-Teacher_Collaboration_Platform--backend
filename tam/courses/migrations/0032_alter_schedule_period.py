# Generated by Django 4.2.3 on 2023-09-26 16:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0031_rename_coustomـtype_schedule_customـtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='period',
            field=models.TimeField(choices=[(datetime.time(0, 5), '5 minutes'), (datetime.time(0, 10), '10 minutes'), (datetime.time(0, 15), '15 minutes'), (datetime.time(0, 20), '20 minutes'), (datetime.time(0, 30), '30 minutes')]),
        ),
    ]
