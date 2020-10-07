# Generated by Django 3.1.1 on 2020-10-06 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_remove_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='grade',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='other_university',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='semester_completed',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('In Progress', 'In Progress')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.student'),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.faculty'),
        ),
    ]
