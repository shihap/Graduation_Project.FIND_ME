# Generated by Django 3.2.5 on 2021-07-10 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20210711_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.CharField(default=None, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.CharField(default=None, max_length=100, null=True, unique=True),
        ),
    ]
