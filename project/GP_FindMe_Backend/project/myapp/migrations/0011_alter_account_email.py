# Generated by Django 3.2.5 on 2021-07-11 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_account_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.CharField(max_length=45, unique=True),
        ),
    ]
