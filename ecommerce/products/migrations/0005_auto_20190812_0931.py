# Generated by Django 2.2.2 on 2019-08-12 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='descrpition',
            field=models.TextField(max_length=1000),
        ),
    ]
