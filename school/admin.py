from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Students_Course)
admin.site.register(Department)
admin.site.register(Major)



# TODO: Electronic Student Record:
#  Add notes in chronological order and allow faculty to change them.
#  Should see date and time and person that changed an entry.

# TODO: allow system to print a copy of student record incluuding information,
#  courses and its information, and gpa