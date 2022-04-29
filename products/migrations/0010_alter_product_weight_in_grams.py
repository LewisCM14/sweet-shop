# Generated by Django 3.2 on 2022-04-28 16:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20220419_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_in_grams',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
    ]