# Generated by Django 3.1.1 on 2020-10-06 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_auto_20201006_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='num_spots',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
