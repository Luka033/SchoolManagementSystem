# Generated by Django 3.1.1 on 2020-10-06 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_auto_20201006_2048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='num_spots',
            new_name='seats_available',
        ),
        migrations.AddField(
            model_name='course',
            name='seats_occupied',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
