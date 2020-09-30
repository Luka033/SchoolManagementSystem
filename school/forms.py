from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['students']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
