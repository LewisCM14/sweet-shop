# Generated by Django 3.2 on 2022-04-12 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_year'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Type',
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name_plural': 'Type'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='type',
        ),
    ]
