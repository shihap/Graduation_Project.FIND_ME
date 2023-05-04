# Generated by Django 3.2.5 on 2021-07-10 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_car_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=45, unique=True)),
                ('password', models.CharField(max_length=45)),
                ('email', models.CharField(default=None, max_length=45)),
                ('profile_picture', models.CharField(default=None, max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default=None, max_length=45)),
                ('date', models.DateField(default=None)),
                ('type', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(default=None, max_length=45)),
                ('phone', models.CharField(default=None, max_length=45)),
                ('account_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.account')),
            ],
        ),
        migrations.CreateModel(
            name='post_images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_dir', models.CharField(default=None, max_length=100)),
                ('post_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='myapp.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user'),
        ),
        migrations.CreateModel(
            name='images_dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(default=None, max_length=100)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]