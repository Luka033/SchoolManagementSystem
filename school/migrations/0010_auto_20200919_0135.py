# Generated by Django 3.1.1 on 2020-09-19 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_auto_20200919_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ForeignKey(default=django.db.models.deletion.SET_NULL, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.student'),
        ),
    ]
