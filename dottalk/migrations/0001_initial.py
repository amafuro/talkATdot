# Generated by Django 4.1 on 2022-09-06 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('last_modify', models.DateTimeField(auto_now=True)),
                ('tweet', models.CharField(max_length=300)),
                ('nickname', models.CharField(max_length=100)),
                ('university_name', models.CharField(max_length=100)),
                ('campus_name', models.CharField(max_length=100)),
                ('good_prog_language', models.CharField(max_length=100)),
                ('bad_prog_language', models.CharField(max_length=100)),
                ('account_image', models.ImageField(blank=True, upload_to='image_directory_path')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('event_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('posted_by', models.CharField(max_length=100)),
                ('posted_by_id', models.IntegerField()),
                ('posted_to_id', models.IntegerField()),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dottalk.account')),
            ],
        ),
    ]
