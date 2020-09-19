from django.db import models

# Create your models here.




class Student(models.Model):

    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    minor = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    # classes = models.ManyToManyField(Course, null=True, blank=True)

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

    course_id = models.CharField(max_length=200, null=True)
    schedule_number = models.CharField(max_length=200, null=True)
    date_time_held = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    instructor = models.CharField(max_length=200, null=True, blank=True)
    units = models.CharField(max_length=200, null=True, choices=NUM_UNITS, default='3')
    prerequisites = models.CharField(max_length=200, null=True, blank=True)

    students = models.ManyToManyField(Student, null=True, blank=True)

    def __str__(self):
        return self.course_id


class Faculty(models.Model):
    name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    office_phone = models.CharField(max_length=200, null=True)
    office_number = models.CharField(max_length=200, null=True)
    office_hours = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200, null=True)





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