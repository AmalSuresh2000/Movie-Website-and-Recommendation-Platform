# Generated by Django 5.0.6 on 2024-05-24 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0002_userprofile_bio_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]
