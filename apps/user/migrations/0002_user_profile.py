# Generated by Django 4.1.4 on 2022-12-16 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='media/profiles/'),
        ),
    ]