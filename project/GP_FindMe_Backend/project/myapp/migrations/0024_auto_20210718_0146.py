# Generated by Django 3.2.5 on 2021-07-17 23:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_auto_20210716_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notfications',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 18, 1, 46, 51, 901027)),
        ),
        migrations.AlterField(
            model_name='post',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 18, 1, 46, 51, 901027)),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=45, unique=True),
        ),
    ]
