# Generated by Django 3.2.5 on 2021-07-17 23:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_auto_20210718_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notfications',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 18, 1, 48, 36, 543148)),
        ),
        migrations.AlterField(
            model_name='post',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 18, 1, 48, 36, 542149)),
        ),
    ]