from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.


class Department(models.Model):
    department_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.department_name

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    major = models.ForeignKey('Major', null=True, blank=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
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
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)

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
    instructor = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)

    semester = models.CharField(max_length=200, null=True)
    course_id = models.CharField(max_length=200, null=True)
    schedule_number = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    time = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    units = models.CharField(max_length=200, null=True, choices=NUM_UNITS, default='3')
    seats_occupied = models.IntegerField(null=True, default=0)
    seats_available = models.IntegerField(null=True, default=25)
    prerequisites = models.ManyToManyField('Course', default="")

    def __str__(self):
        return self.course_id


class Students_Course(models.Model):
    STATUS = (
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
    )

    GRADE = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    )

    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    semester_completed = models.CharField(max_length=200, null=True, blank=True)
    grade = models.CharField(max_length=200, null=True, choices=GRADE, blank=True)
    other_university = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.student.name + " - " + self.course.course_id



class Major(models.Model):
    major_title = models.CharField(max_length=200, null=True)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    units_for_major = models.CharField(max_length=200, null=True)
    required_courses = models.ManyToManyField(Course, related_name='required_courses')
    electives = models.ManyToManyField(Course, related_name='electives')

    def __str__(self):
        return self.major_title

