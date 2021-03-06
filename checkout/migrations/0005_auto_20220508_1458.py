# Generated by Django 3.2 on 2022-05-08 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20220508_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='original_bag',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_pid',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='order',
            name='full_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
