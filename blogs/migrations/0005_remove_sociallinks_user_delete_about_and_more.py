# Generated by Django 5.1 on 2024-08-17 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_about_sociallinks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sociallinks',
            name='user',
        ),
        migrations.DeleteModel(
            name='About',
        ),
        migrations.DeleteModel(
            name='Sociallinks',
        ),
    ]
