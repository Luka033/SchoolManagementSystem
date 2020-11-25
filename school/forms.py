from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from school.models import CustomUser, Student, Faculty
from django.db import transaction


# 1/Overriding the built-in UserCreationForm
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'address')


# 2/Overriding the built-in UserChangeForm
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'address')


class StudentSignUpForm(UserCreationForm):

    class Meta(CustomUserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()

        student = Student.objects.create(user=user)
        student.name = user.first_name + ' ' + user.last_name
        student.date_of_birth = user.date_of_birth
        student.address = user.address
        student.email = user.email
        student.save()

        return user


class FacultySignUpForm(UserCreationForm):

    class Meta(CustomUserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_faculty = True
        user.save()

        faculty = Faculty.objects.create(user=user)
        faculty.name = user.first_name + ' ' + user.last_name
        faculty.date_of_birth = user.date_of_birth
        faculty.title = 'Teacher'
        faculty.address = user.address
        faculty.email = user.email
        faculty.save()

        return user


class UpdateStudentDetailForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']


class UpdateFacultyDetailForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user']

class UpdateStudentOutlineForm(ModelForm):
    class Meta:
        model = Student_Outline
        fields = '__all__'
        exclude = ['student', 'course', 'date_edited', 'edited_by']


class GradeForm(ModelForm):
    class Meta:
        model = Students_Course
        fields = ['grade']


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['students']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
