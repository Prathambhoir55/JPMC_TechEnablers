# Generated by Django 4.1.7 on 2023-03-18 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='is_end',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='location',
            name='is_start',
            field=models.BooleanField(default=False),
        ),
    ]
