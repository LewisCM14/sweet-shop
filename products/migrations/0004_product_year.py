# Generated by Django 3.2 on 2022-04-12 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20220412_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='year',
            field=models.IntegerField(choices=[(0, '90s & 00s'), (1, '90s'), (2, '00s')], default=0),
        ),
    ]
