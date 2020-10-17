# Generated by Django 3.1.1 on 2020-10-15 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_auto_20201015_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='prerequisites',
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(to='school.Course'),
        ),
    ]