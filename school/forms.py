from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

from django import forms


class GradeForm(ModelForm):
    class Meta:
        model = Students_Course
        fields = ['grade']


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['students']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']


class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
