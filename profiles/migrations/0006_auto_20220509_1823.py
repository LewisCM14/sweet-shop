# Generated by Django 3.2 on 2022-05-09 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20220506_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_first_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_last_name',
            new_name='last_name',
        ),
    ]
