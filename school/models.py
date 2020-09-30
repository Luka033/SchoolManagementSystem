from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    minor = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name



class Faculty(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    office_phone = models.CharField(max_length=200, null=True)
    office_number = models.CharField(max_length=200, null=True)
    office_hours = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    NUM_UNITS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    instructor = models.ForeignKey(Faculty, null=True, on_delete= models.SET_NULL)
    students = models.ManyToManyField(Student, null=True, blank=True)

    course_id = models.CharField(max_length=200, null=True)
    schedule_number = models.CharField(max_length=200, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    time = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    units = models.CharField(max_length=200, null=True, choices=NUM_UNITS, default='3')
    prerequisites = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.course_id






# class Major(models.Model):
#     major_id = models.CharField(max_length=200, null=True)
#     major_title = models.CharField(max_length=200, null=True)
#     department = models.CharField(max_length=200, null=True)
#     units_for_major = models.CharField(max_length=200, null=True)
#     required_courses = models.CharField(max_length=200, null=True)
#     elective_courses = models.CharField(max_length=200, null=True)
#     advisors_for_major = models.CharField(max_length=200, null=True)
#
#     def __str__(self):
#         return self.course_id