# Generated by Django 3.2.5 on 2021-07-11 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20210711_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user_name',
            field=models.CharField(max_length=45),
        ),
    ]
