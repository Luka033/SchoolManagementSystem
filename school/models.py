import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Department(models.Model):

    department_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.department_name

    def get_absolute_url(self):
        return reverse('department_detail', kwargs={'pk': self.pk})


class CustomUser(AbstractUser):

    date_of_birth = models.DateField(default=timezone.now)
    phone_number = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)


class Student(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    major = models.ForeignKey('Major', null=True, blank=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(default=timezone.now)
    address = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    minor = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    graduate_student = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class Faculty(models.Model):

    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(default=timezone.now)
    address = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True)
    office_phone = models.CharField(max_length=200, null=True)
    office_number = models.CharField(max_length=200, null=True)
    office_hours = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('faculty_detail', kwargs={'pk': self.pk})


class Course(models.Model):
    NUM_UNITS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    COURSE_LEVEL = (
        ('Lower-division', 'Lower-division'),
        ('Upper-division', 'Upper-division'),
        ('Graduate', 'Graduate'),
    )

    course_id = models.CharField(max_length=200, null=True)
    schedule_number = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    units = models.CharField(max_length=200, null=True, choices=NUM_UNITS, default='3')
    time = models.CharField(max_length=200, null=True)
    day = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    instructor = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    capacity = models.IntegerField(null=True, default=0)
    seats_open = models.IntegerField(null=True, default=capacity)
    course_level = models.CharField(max_length=200, null=True, choices=COURSE_LEVEL, default='Lower-division')

    semester = models.CharField(max_length=200, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    prerequisites = models.ManyToManyField('Course', blank=True, default="")

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
    TERM = (
        ('SP19', 'SP19'),
        ('FA19', 'Fa')
    )

    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    university = models.CharField(max_length=200, null=True, blank=True, default="San Diego State University")
    university_location = models.CharField(max_length=200, null=True, blank=True, default="San Diego")
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    semester_completed = models.CharField(max_length=200, null=True, blank=True)
    grade = models.CharField(max_length=200, null=True, choices=GRADE, blank=True)

    def __str__(self):
        return self.student.name + " - " + self.course.course_id


class Student_Outline(models.Model):
    STATUS = (
        ('Approved', 'Approved'),
        ('Waived', 'Waived'),
        ('Dropped', 'Dropped')
    )

    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    notes = models.CharField(max_length=200, null=True, blank=True)
    date_edited = models.DateTimeField(default=timezone.now, null=True)
    edited_by = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.student.name + "'s Outline: " + self.course.course_id


class Major(models.Model):

    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    required_courses = models.ManyToManyField(Course, related_name='required_by_majors')
    electives = models.ManyToManyField(Course, related_name='electives')

    major_title = models.CharField(max_length=200, null=True)
    units_for_major = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.major_title

    # def get_absolute_url(self):
    #     return reverse('major_detail', kwargs={'pk': self.pk})