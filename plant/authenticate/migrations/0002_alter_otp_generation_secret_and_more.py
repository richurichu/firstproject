# Generated by Django 4.2.2 on 2023-07-01 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp_generation',
            name='secret',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='otp_generation',
            name='tokens',
            field=models.CharField(max_length=10),
        ),
    ]
