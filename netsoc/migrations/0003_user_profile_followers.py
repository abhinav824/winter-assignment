# Generated by Django 2.1.3 on 2018-12-25 01:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('netsoc', '0002_auto_20181224_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='followers',
            field=models.ManyToManyField(related_name='following_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
