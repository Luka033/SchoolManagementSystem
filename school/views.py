from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.urls import reverse_lazy

from .models import *
from .forms import CourseForm, CreateUserForm, GradeForm, UpdateFacultyDetailForm, \
    UpdateStudentDetailForm
from .filters import CourseFilter, FacultyFilter, StudentFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.views.generic import CreateView, DetailView, ListView
from school.forms import CustomUserCreationForm, StudentSignUpForm, FacultySignUpForm
from school.models import Student, Faculty


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                            SIGN UP
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


'''______________________________ STUDENT SIGNUP view ___________________________________'''


class StudentSignUpView(CreateView):
    """ Class-base: STUDENT SIGN UP view """

    model = Student
    form_class = StudentSignUpForm
    template_name = 'registration/signup_student_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


'''______________________________ FACULTY SIGNUP view ___________________________________'''


class FacultySignUpView(CreateView):
    """ Class-base: FACULTY SIGN UP view """

    model = Faculty
    form_class = FacultySignUpForm
    template_name = 'registration/signup_faculty_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'faculty'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                       CATALOG VIEW
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


'''___________________________ FACULTY CATALOG view ___________________________'''


@login_required(login_url='login')
def catalog_faculty(request):
    """ Function-base: FACULTY CATALOG view """

    faculty_list = Faculty.objects.all()

    my_filter = FacultyFilter(request.GET, queryset=faculty_list)
    faculty_list = my_filter.qs
    context = {
        'faculty_list': faculty_list,
        'filter': my_filter
    }
    return render(request, 'school/catalog_faculty.html', context)


class FacultyListView(ListView):
    """ Class-base: FACULTY CATALOG view """

    model = Faculty
    context_object_name = 'faculty_list'
    template_name = 'school/catalog_faculty.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # context['_list'] = context.

        return context


'''__________________________ STUDENT CATALOG view_________________________'''


@login_required(login_url='login')
def catalog_student(request):
    """ Function-base: STUDENT CATALOG view """

    student_list = Student.objects.all()

    my_filter = StudentFilter(request.GET, queryset=student_list)
    student_list = my_filter.qs
    context = {
        'student_list': student_list,
        'filter': my_filter
    }
    return render(request, 'school/catalog_student.html', context)


'''_________________________ UPDATE PERSONAL INFO view ____________________________'''


@login_required(login_url='login')
def update_personal_info(request):

    if request.user.is_faculty:

        faculty = request.user.faculty
        form = UpdateFacultyDetailForm(instance=faculty)

        if request.method == 'POST':  # It doesn't access this condition so the updates won't occur
            faculty = Faculty.objects.get(id=faculty.id)
            form = UpdateFacultyDetailForm(request.POST, instance=faculty)
            if form.is_valid():
                form.save()
                return redirect('faculty_detail')

    elif request.user.is_student:
        student = request.user.student
        print(student)
        form = UpdateStudentDetailForm(instance=student)

        if request.method == 'POST':  # It doesn't access this condition so the updates won't occur
            student = Student.objects.get(id=student.id)
            form = UpdateStudentDetailForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect('student_detail')

    context = {
        'form': form
    }
    return render(request, 'school/update_personal_info_form.html', context)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             STUDENT
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

'''___________________________ STUDENT HOME view ___________________________'''


@login_required(login_url='login')
def student_home(request):
    """ Function-base: STUDENT HOME view """

    id = request.user.student.id
    student = Student.objects.get(id=id)

    completed_courses = student.students_course_set.filter(status="Completed")
    in_progress_courses = student.students_course_set.filter(status="In Progress")

    student_grades = list(completed_courses.values("grade"))

    student_gpa = grade_converter(student_grades)

    context = {
        'student': student,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses,
        'student_gpa': student_gpa
    }
    return render(request, 'school/student_detail.html', context)


'''___________________________ STUDENT DETAIL view ___________________________'''


@login_required(login_url='login')
def student_detail(request):
    """ Function-base: STUDENT DETAIL view """

    student = request.user.student
    completed_courses = student.students_course_set.filter(status="Completed")
    in_progress_courses = student.students_course_set.filter(status="In Progress")

    context = {
        'student': student,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses
        }
    return render(request, 'school/student_detail.html', context)


class StudentDetailView(DetailView):
    model = Student
    context_obj_name = 'student'
    template_name = 'school/student_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['completed_courses'] = context.students_course_set.filter(status="Completed")
        context['in_progress_courses'] = context.students_course_set.filter(status="In Progress")
        return context


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             FACULTY
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


'''________________________________ FACULTY HOME view _______________________________'''


@login_required(login_url='login')
def faculty_home(request):
    """ Function-base: FACULTY HOME view """

    context = {
        'faculty': request.user.faculty,
    }
    return render(request, 'school/faculty_home.html', context)


class FacultyHomeView(DetailView):
    """ Class-based: FACULTY HOME view """

    model = Faculty
    context_object_name = 'faculty'
    template_name = 'school/faculty_detail.html'


'''________________________________ FACULTY DETAIL view _______________________________'''


@login_required(login_url='login')
def faculty_detail(request):
    """ Function-base: FACULTY DETAIL view """
    context = {
        'faculty': request.user.faculty,
    }
    return render(request, 'school/faculty_detail.html', context)


class FacultyDetailView(DetailView):
    """ Class-based: FACULTY DETAIL view """

    model = Faculty
    context_object_name = 'faculty'
    template_name = 'school/faculty_detail.html'


'''________________________________ FACULTY COURSE view ________________________________'''


@login_required(login_url='login')
def teaching_schedule(request):
    """ Function-base: FACULTY COURSE view """

    faculty = request.user.faculty
    courses = Course.objects.filter(instructor=faculty.id)

    context = {
        'faculty': faculty,
        'courses': courses,
    }
    return render(request, 'school/teaching_schedule.html', context)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             GRADE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

'''_____________________________ COURSE GRADE view _________________________________'''


@login_required(login_url='login')
def course_grades(request):
    faculty = request.user.faculty
    courses = faculty.course_set.all()

    student_course_dic = {}
    for course in courses:
        student_list = Students_Course.objects.filter(course=course)
        student_course_dic[course.course_id] = student_list

    context = {
        'student_course_dic': student_course_dic
    }
    return render(request, 'school/course_grades.html', context)


def update_grade(request, pk):
    form = GradeForm()

    if request.method == 'POST':  # It doesn't access this condition so the updates won't occur
        student_course = Students_Course.objects.get(id=pk)
        form = GradeForm(request.POST, instance=student_course)
        if form.is_valid():
            form.save()
            return redirect('../course_grades')

    context = {
        'form': form,
    }
    return render(request, 'school/update_grade.html', context)


# This section manages views concerning STUDENTS ONLY
# =============================================================
# =============================================================
def grade_converter(student_grades):
    # TODO: Move dict and/or function
    grade_values = {
        'A': 4.0,
        'B': 3.0,
        'C': 2.0,
        'D': 1.0,
        'F': 0.0
    }
    if len(student_grades) > 0:
        gpa = 0.0
        for grade in student_grades:
            letter_grade = str(grade['grade'])
            gpa += grade_values[letter_grade]

        return gpa / len(student_grades)
    else:
        return 0.0


"""
____________________________________________________________________________
                                COURSE
____________________________________________________________________________
"""


class CourseListView(ListView):
    model = Course
    template_name = 'catalog/courses_list.html'


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
    id = request.user.student.id
    student = Student.objects.get(id=id)
    completed_courses = []
    prereq = course.prerequisites.all()
    students_completed_courses = student.students_course_set.filter(status="Completed")
    for i in students_completed_courses:
        completed_courses.append(i.course)

    if student.students_course_set.filter(course=course).exists():
        messages.info(request, 'You are already enrolled or have completed ' + course.course_id)
        return redirect('course_registration')

    if course.seats_occupied + 1 > course.seats_available:
        messages.info(request, course.course_id + " has no available seats")
        return redirect('course_registration')

    majors = course.required_by_majors.all()
    if course.course_level == "Upper-division" and majors:
        if student.major not in majors:
            messages.info(request, course.course_id + " is restricted to students of that declared major only")
            return redirect('course_registration')

    if course.course_level == "Graduate" and not student.graduate_student:
        messages.info(request, course.course_id + " is for Graduate students only")
        return redirect('course_registration')

    if not all(x in completed_courses for x in prereq):
        messages.info(request, 'You have not met the prerequisites for ' + course.course_id)
        return redirect('course_registration')
    else:
        if request.method == 'POST':
            new_student_class = Students_Course(student=student, course=course, status="In Progress")
            new_student_class.save()

            course.seats_occupied += 1
            course.save()

            return redirect('course_registration')

    context = {'course': course}
    return render(request, 'school/add_course.html', context)


@login_required(login_url='login')
def drop_course(request, pk):
    print(pk)
    course = Course.objects.get(id=pk)
    id = request.user.student.id
    student = Student.objects.get(id=id)
    class_to_drop = student.students_course_set.filter(course=course)
    num_students = Students_Course.objects.filter(course=course).count()

    if request.method == 'POST':
        class_to_drop.delete()

        course.seats_occupied = num_students - 1
        course.save()

        return redirect('student_home')

    context = {'course': course}
    return render(request, 'school/drop_course.html', context)


# This section manages views concerning STUDENTS and FACULTY
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
def majors(request):
    majors = Major.objects.all().order_by('department')

    context = {'majors': majors}
    return render(request, 'school/majors.html', context)


def major_requirements_details(request, pk):
    major = Major.objects.get(id=pk)
    required_courses = major.required_courses.all()
    electives = major.electives.all()
    context = {'major': major,
               'required_courses': required_courses,
               'electives': electives
               }
    return render(request, 'school/major_requirements_details.html', context)