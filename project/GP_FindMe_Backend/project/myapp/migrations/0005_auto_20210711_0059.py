# Generated by Django 3.2.5 on 2021-07-10 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_relatives'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relatives',
            name='relative_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relative_id', to='myapp.user'),
        ),
        migrations.AlterField(
            model_name='relatives',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='myapp.user'),
        ),
    ]
