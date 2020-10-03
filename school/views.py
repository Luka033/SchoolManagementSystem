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
def faculty_details(request, pk):
    faculty = Faculty.objects.get(id=pk)
    courses = Course.objects.filter(instructor=pk)
    print(courses)

    context = {'faculty': faculty,
               'courses': courses}
    return render(request, 'school/faculty_details.html', context)


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
def student_details(request, pk):
    student = Student.objects.get(id=pk)
    courses = Course.objects.filter(students=pk)

    context = {'student': student,
               'courses': courses
               }
    return render(request, 'school/student_details.html', context)


@login_required(login_url='login')
def course_grades(request):
    faculty_member = Faculty.objects.get(id=request.user.id)
    courses_teaching = faculty_member.course_set.all()

    students_in_courses = {}
    for i in range(len(courses_teaching)):

        students = courses_teaching[i].students.all()
        students_in_courses[courses_teaching[i]] = students
        print(students_in_courses)

    context = {'students_in_courses': students_in_courses}
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
def student_home(request):
    id = request.user.student.id
    student = Student.objects.get(id=id)
    courses = Course.objects.filter(students=id)

    context = {'student': student,
               'courses': courses
               }
    return render(request, 'school/student_details.html', context)


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




# This section manages views available for STUDENTS and FACULTY
# =============================================================
# =============================================================
def major_course_requirements(request):
    return render(request, 'school/major_requirements.html')


@login_required(login_url='login')
def course_details(request, pk):
    course = Course.objects.get(id=pk)
    print(course)

    context = {'course': course}
    return render(request, 'school/course_details.html', context)











@login_required(login_url='login')
def drop_course(request, pk):
    course = Course.objects.get(id=pk)
    # if request.method == 'POST':
    #     course.delete()
    #     return redirect('/')

    context = {'course': course}
    return render(request, 'school/drop_course.html', context)



