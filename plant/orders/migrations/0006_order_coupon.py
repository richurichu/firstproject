# Generated by Django 4.2.3 on 2023-08-01 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_original_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.FloatField(null=True),
        ),
    ]