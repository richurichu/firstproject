# Generated by Django 4.2.2 on 2023-07-08 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
