# Generated by Django 2.2.2 on 2019-09-02 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20190901_0741'),
        ('order', '0004_auto_20190901_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.Billingprofile'),
        ),
    ]
