# Generated by Django 2.2.2 on 2019-08-12 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_featured'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='descrpition',
            new_name='descripition',
        ),
    ]
