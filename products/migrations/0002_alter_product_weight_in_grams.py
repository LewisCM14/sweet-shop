# Generated by Django 3.2 on 2022-04-12 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_in_grams',
            field=models.IntegerField(),
        ),
    ]
