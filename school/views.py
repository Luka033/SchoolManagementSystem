from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CourseForm, StudentForm, FacultyForm, CreateUserForm
from .filters import CourseFilter, FacultyFilter, StudentFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


# This section manages registration, login, and logout
# =============================================================
# =============================================================
@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('faculty_home')
        else:
            messages.info(request, 'Username or Password is incorrect!')

    context = {}
    return render(request, 'school/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='student')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'school/register.html', context)






# This section manages dashboard, FCI, ER, Course Grades and Account Settings for FACULTY
# =============================================================
# =============================================================
@login_required(login_url='login')
@admin_only
def faculty_home(request):
    students = Student.objects.all()
    courses = Course.objects.all()

    context = {'students': students,
               'courses': courses,
               }
    return render(request, 'school/faculty_home.html', context)


@login_required(login_url='login')
def faculty_course_info(request):
    faculty_members = Faculty.objects.all()

    my_filter = FacultyFilter(request.GET, queryset=faculty_members)
    faculty_members = my_filter.qs
    context = {'faculty_members': faculty_members,
               'filter': my_filter
               }
    return render(request, 'school/faculty_course_info.html', context)


@login_required(login_url='login')
def electronic_student_record(request):
    all_students = Student.objects.all()

    my_filter = StudentFilter(request.GET, queryset=all_students)
    all_students = my_filter.qs
    context = {'all_students': all_students,
               'filter': my_filter
               }
    return render(request, 'school/electronic_student_record.html', context)


@login_required(login_url='login')
def student(request, pk):
    student = Student.objects.get(id=pk)
    courses = Course.objects.filter(students=pk)

    context = {'student': student,
               'courses': courses
               }
    return render(request, 'school/student.html', context)


@login_required(login_url='login')
def course_grades(request):
    faculty_member = Faculty.objects.get(id=request.user.id)
    courses_teaching = faculty_member.course_set.all()
    context = {'courses': courses_teaching}
    return render(request, 'school/course_grades.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['student'])
def account_settings(request):
    faculty = request.user.faculty
    form = FacultyForm(instance=faculty)
    context = {'form': form}
    return render(request, 'school/account_settings.html', context)






# This section manages dashboard, course registration and account settings for STUDENTS
# =============================================================
# =============================================================
@login_required(login_url='login')
def user_page(request):
    id = request.user.student.id
    student = Student.objects.get(id=id)
    courses = Course.objects.filter(students=id)

    context = {'student': student,
               'courses': courses
               }
    return render(request, 'school/student.html', context)


@login_required(login_url='login')
def course_registration(request):
    courses = Course.objects.all()

    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs
    context = {'courses': courses,
               'filter': my_filter
               }
    return render(request, 'school/course_registration.html', context)


@login_required(login_url='login')
def add_course(request, pk):
    course = Course.objects.get(id=pk)
    # if request.method == 'POST':
    #     course.save()
    #     return redirect('/')

    context = {'course': course}
    return render(request, 'school/add_course.html', context)




# This section manages Major Requirements
# =============================================================
# =============================================================
def major_course_requirements(request):
    return render(request, 'school/major_requirements.html')






# This section manages CRUD for STUDENTS
# =============================================================
# =============================================================
@login_required(login_url='login')
def create_student(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school/create_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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
@login_required(login_url='login')
def create_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'school/create_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_course(request, pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('/')

    context = {'course': course}
    return render(request, 'school/delete_course.html', context)



