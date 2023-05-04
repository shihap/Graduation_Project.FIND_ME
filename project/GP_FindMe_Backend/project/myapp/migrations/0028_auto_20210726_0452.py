# Generated by Django 3.2.5 on 2021-07-26 02:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_auto_20210726_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notfications',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 4, 52, 20, 81110)),
        ),
        migrations.AlterField(
            model_name='post',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 4, 52, 20, 80113)),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_dir',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.CharField(default=None, max_length=1000, null=True, unique=True),
        ),
    ]
