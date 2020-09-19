# Generated by Django 3.1.1 on 2020-09-19 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_auto_20200919_0009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='student',
        ),
        migrations.AddField(
            model_name='student',
            name='classes',
            field=models.ManyToManyField(blank=True, null=True, to='school.Course'),
        ),
    ]
