from django.forms import ModelForm
from .models import *

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['students']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
