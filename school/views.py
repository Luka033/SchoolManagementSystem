from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import CourseForm, StudentForm
from .filters import CourseFilter


# Create your views here.
def home(request):
    students = Student.objects.all()
    total_students = students.count()

    courses = Course.objects.all()
    total_courses = courses.count()

    context = {'students': students,
               'total_students': total_students,
               'courses': courses,
               'total_courses': total_courses,
               }
    return render(request, 'school/dashboard.html', context)


def faculty(request):
    return render(request, 'school/faculty.html')


def student(request, pk):
    student = Student.objects.get(id=pk)
    courses = Course.objects.filter(students=pk)

    context = {'student': student,
               'courses': courses
               }
    return render(request, 'school/student.html', context)


def major_course_requirements(request):
    return render(request, 'school/major_requirements.html')




# This section manages CRUD for STUDENTS
# =============================================================
# =============================================================
def create_student(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school/create_form.html', context)


def update_student(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'school/create_form.html', context)


def delete_student(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/')

    print("STUDENT IS: ", student)
    context = {'student': student}
    return render(request, 'school/delete_student.html', context)


# This section manages CRUD for COURSES
# =============================================================
# =============================================================
def create_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school/create_form.html', context)


def update_course(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school/create_form.html', context)


def delete_course(request, pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('/')

    context = {'course': course}
    return render(request, 'school/delete_course.html', context)




def course_registration(request):
    courses = Course.objects.all()

    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs



    context = {'courses': courses,
               'filter': my_filter
               }
    return render(request, 'school/course_registration.html', context)