# Generated by Django 3.2 on 2022-05-08 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20220506_1515'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
    ]
