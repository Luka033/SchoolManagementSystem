# Generated by Django 3.1.1 on 2020-10-15 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_course_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_title', models.CharField(max_length=200, null=True)),
                ('units_for_major', models.CharField(max_length=200, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.department')),
                ('required_courses', models.ManyToManyField(to='school.Course')),
            ],
        ),
    ]
