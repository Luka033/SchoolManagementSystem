from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from school.forms import CustomUserCreationForm, CustomUserChangeForm
from school.models import *


# Extend the existing UserAdmin class to our CustomUser model
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Display these attributes in admin site
    list_display = ['id', 'email', 'username', 'is_staff', 'is_student', 'is_faculty', ]


# Register out new CustomUserAdmin in the admin site
admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Students_Course)
admin.site.register(Student_Outline)
admin.site.register(Department)
admin.site.register(Major)


# TODO: Electronic Student Record:
#  Add notes in chronological order and allow faculty to change them.
#  Should see date and time and person that changed an entry.

# TODO: allow system to print a copy of student record including information,
#  courses and its information, and gpa
