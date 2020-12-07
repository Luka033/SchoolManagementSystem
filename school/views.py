import pytz
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
    UpdateStudentDetailForm, UpdateStudentOutlineForm
from .filters import CourseFilter, FacultyFilter, StudentFilter

from django.views.generic import CreateView, DetailView, ListView
from school.forms import CustomUserCreationForm, StudentSignUpForm, FacultySignUpForm
from school.models import Student, Faculty

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


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
New Section:                       CATALOG
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


'''___________________________ FACULTY CATALOG view ___________________________'''


def catalog_faculty(request):
    """ Function-base: FACULTY CATALOG view """

    faculty_list = Faculty.objects.all()

    my_filter = FacultyFilter(request.GET, queryset=faculty_list)
    faculty_list = my_filter.qs
    context = {
        'faculty_list': faculty_list,
        'filter': my_filter
    }
    return render(request, 'school/catalog/faculty_list.html', context)


class FacultyListView(ListView):
    """ Class-base: FACULTY CATALOG view """

    model = Faculty
    context_object_name = 'faculty_list'
    template_name = 'school/catalog/faculty_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # context['_list'] = context.

        return context


'''__________________________ STUDENT CATALOG view_________________________'''


@login_required(login_url='login')
def catalog_student(request):
    """ Function-based: STUDENT CATALOG view """

    student_list = Student.objects.all()

    my_filter = StudentFilter(request.GET, queryset=student_list)
    student_list = my_filter.qs
    context = {
        'student_list': student_list,
        'filter': my_filter
    }
    return render(request, 'school/catalog/student_list.html', context)


'''__________________________ COURSE CATALOG view_________________________'''


class CourseListView(ListView):
    """ Class-based: COURSE CATALOG view """
    model = Course
    template_name = 'school/catalog/course_list.html'


def catalog_course(request):
    courses = Course.objects.all()

    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs
    context = {
        'courses': courses,
        'filter': my_filter
    }
    return render(request, 'school/catalog/course_list.html', context)


'''__________________________ MAJOR CATALOG view_________________________'''


# class MajorListView(DetailView):
#     """ Class-based: MAJOR CATALOG view """
#     model = Major
#     context_object_name = 'major_list'
#     template_name = 'school/catalog/major_list.html'
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#
#
#         return context


def catalog_major(request):
    """ Function-based: MAJOR CATALOG view """
    major_list = Major.objects.all()

    major_dict = {major: major.required_courses.all() for major in major_list}

    return render(request, 'school/catalog/major_list.html', {'major_dict': major_dict})


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             MAJOR
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def major_course_requirements(request):
    return render(request, 'school/major/major_requirements.html')


def major_requirement(request, pk):
    major = Major.objects.get(id=pk)
    required_courses = major.required_courses.all()
    electives = major.electives.all()

    context = {
        'major': major,
        'required_courses': required_courses,
        'electives': electives
    }
    return render(request, 'school/catalog/major_requirements.html', context)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             ACCOUNT
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


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
                return redirect('faculty_detail', faculty.id)

    elif request.user.is_student:
        student = request.user.student
        form = UpdateStudentDetailForm(instance=student)

        if request.method == 'POST':  # It doesn't access this condition so the updates won't occur
            student = Student.objects.get(id=student.id)
            form = UpdateStudentDetailForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect('student_detail', student.id)

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

    context = {

        'student': student,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses,

    }
    return render(request, 'school/student/home.html', context)


'''___________________________ STUDENT DETAIL view ___________________________'''


@login_required(login_url='login')
def student_detail(request, pk):
    """ Function-base: STUDENT DETAIL view """

    student = Student.objects.get(id=pk)
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
    return render(request, 'school/student/detail.html', context)


@login_required(login_url='login')
def student_outline(request, pk):
    """ Function-base: STUDENT OUTLINE view """

    student = Student.objects.get(id=pk)
    student_outline = student.student_outline_set.all()

    department = student.major.department
    possible_outline_courses = Course.objects.filter(department=department)

    context = {
        'student': student,
        'student_outline': student_outline,
        'possible_outline_courses': possible_outline_courses
    }
    return render(request, 'school/student/outline.html', context)


@login_required(login_url='login')
def edit_student_outline(request, pk, pk2):
    if request.user.is_faculty:
        faculty = request.user.faculty
        student = Student.objects.get(id=pk2)
        student_outline = Student_Outline.objects.get(id=pk)

        form = UpdateStudentOutlineForm(instance=student_outline)

        if request.method == 'POST':  # It doesn't access this condition so the updates won't occur
            form = UpdateStudentOutlineForm(request.POST, instance=student_outline)
            if form.is_valid():
                student_outline.date_edited = timezone.now()
                form.save()
                return redirect('student_outline', student.id)

    context = {
        'form': form,
        'student': student,
        'student_outline': student_outline
    }
    return render(request, 'school/edit_student_outline.html', context)


@login_required(login_url='login')
def add_outline_course(request, pk, pk2):
    course = Course.objects.get(id=pk)
    student = Student.objects.get(id=pk2)
    faculty_name = request.user.faculty

    if Student_Outline.objects.filter(course=course).exists():
        messages.info(request, course.course_id + " is already in the " + student.name + "'s Major outline")
        return redirect('student_outline', student.id)
    if Students_Course.objects.filter(course=course).exists():
        messages.info(request, student.name + " is already enrolled in or has completed " + course.course_id)
        return redirect('student_outline', student.id)
    else:
        if request.method == 'POST':
            new_student_outline_class = Student_Outline(student=student,
                                                        course=course,
                                                        status="Approved",
                                                        edited_by=faculty_name)
            new_student_outline_class.save()
            return redirect('student_outline', student.id)

    context = {'course': course,
               'student': student}
    return render(request, 'school/add_outline_course.html', context)


@login_required(login_url='login')
def remove_outline_course(request, pk, pk2):
    course = Course.objects.get(id=pk)
    student = Student.objects.get(id=pk2)
    outline_course_to_delete = Student_Outline.objects.get(course=course)

    if request.method == 'POST':
        outline_course_to_delete.delete()

        return redirect('student_outline', student.id)

    context = {'course': course,
               'student': student}
    return render(request, 'school/remove_outline_course.html', context)


class StudentDetailView(DetailView):
    model = Student
    context_obj_name = 'student'
    template_name = 'school/student/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['completed_courses'] = context.students_course_set.filter(status="Completed")
        context['in_progress_courses'] = context.students_course_set.filter(status="In Progress")
        return context


'''___________________________ STUDENT SCHEDULE view ___________________________'''


class StudentScheduleView(DetailView):
    model = Student
    context_obj_name = 'student'
    template_name = 'school/student/schedule.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['completed_courses'] = context.students_course_set.filter(status="Completed")
        context['in_progress_courses'] = context.students_course_set.filter(status="In Progress")
        return context


@login_required(login_url='login')
def student_schedule(request, pk):
    """ Function-base: STUDENT Schedule view """

    student = Student.objects.get(id=pk)
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
    return render(request, 'school/student/schedule.html', context)


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
    return render(request, 'school/faculty/home.html', context)


class FacultyHomeView(DetailView):
    """ Class-based: FACULTY HOME view """

    model = Faculty
    context_object_name = 'faculty'
    template_name = 'school/faculty/home.html'


'''________________________________ FACULTY DETAIL view _______________________________'''


@login_required(login_url='login')
def faculty_detail(request, pk):
    """ Function-base: FACULTY DETAIL view """
    faculty = Faculty.objects.get(id=pk)
    context = {
        'faculty': faculty,
    }
    return render(request, 'school/faculty/detail.html', context)


class FacultyDetailView(DetailView):
    """ Class-based: FACULTY DETAIL view """

    model = Faculty
    context_object_name = 'faculty'
    template_name = 'school/faculty/detail.html'


'''________________________________ FACULTY COURSE view ________________________________'''


@login_required(login_url='login')
def faculty_schedule(request):
    """ Function-base: FACULTY COURSE view """

    faculty = request.user.faculty
    courses = Course.objects.filter(instructor=faculty.id)

    context = {
        'faculty': faculty,
        'courses': courses,
    }
    return render(request, 'school/faculty/schedule.html', context)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             COURSE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


'''_____________________________ Course DETAIL view _________________________________'''


@login_required(login_url='login')
def course_details(request, pk):
    course = Course.objects.get(id=pk)
    prerequisites = course.prerequisites.all()

    context = {'course': course,
               'prerequisites': prerequisites}
    return render(request, 'school/course/detail.html', context)


'''_____________________________ COURSE REGISTRATION view _________________________________'''


@login_required(login_url='login')
def course_registration(request):
    courses = Course.objects.all()

    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs
    context = {'courses': courses,
               'filter': my_filter
               }
    return render(request, 'school/course/registration.html', context)


'''_____________________________ ADD COURSE view _________________________________'''


@login_required(login_url='login')
def add_course(request, pk):
    user = request.user
    course = Course.objects.get(id=pk)

    if user.is_student and request.method == 'POST':

        student = Student.objects.get(id=user.student.id)
        completed_courses = [i.course for i in student.students_course_set.filter(status="Completed")]

        # Cannot enroll if student already completed this course in previous term
        if course in completed_courses:
            messages.info(request, 'You have already completed ' + course.course_id)

        # Cannot enroll if already enrolled in this section at current term
        elif student.students_course_set.filter(course=course).exists():
            messages.info(request, 'You are already enrolling in ' + course.course_id)

        # Cannot enroll if the section is full
        elif course.seats_open == 0:
            messages.info(request, course.course_id + " has no available seats")

        # Cannot enroll in a upper division if student doesnt declared
        elif course.course_level == "Under-graduate" and student.major not in majors:
            messages.info(request, 'Your Major/Minor is not allowed in' + course.course_id)

        # Cannot enroll in Graduate course if still in undergrad
        elif course.course_level == "Graduate" and not student.graduate_student:
            messages.info(request, course.course_id + " is for Graduate students only")

        # Cannot enroll if student does not meet the prerequisites:
        elif not all(x in completed_courses for x in course.prerequisites.all()):
            messages.info(request, 'You have not met the prerequisites for ' + course.course_id +
                          '. Please check the prerequisites note for this course.')

        # Else allow student to enroll
        else:
            new_student_class = Students_Course(student=student, course=course, status="In Progress")
            new_student_class.save()

            # Seats_open cannot be negative
            if course.seats_open > 0:
                course.seats_open -= 1

            course.save()
            messages.info(request, 'Successfully enrolled in ' + course.course_id)

        return redirect('course_registration')

    return render(request, 'school/course/add_course.html', {'course': course})


'''_____________________________ DROP Course view _________________________________'''


@login_required(login_url='login')
def drop_course(request, pk):
    user = request.user
    student = Student.objects.get(id=user.student.id)
    course = Course.objects.get(id=pk)
    class_to_drop = student.students_course_set.get(course=pk)

    if request.method == 'POST':
        class_to_drop.delete()

        # Seats_open cannot be greater than capacity
        if course.seats_open <= course.capacity:
            course.seats_open += 1

        course.save()
        messages.info(request, 'Successfully dropped ' + course.course_id)
        return redirect('student_schedule', user.student.id)

    context = {
        'course': course
    }
    return render(request, 'school/course/drop_course.html', context)


'''_____________________________ END Course view _________________________________'''


@login_required(login_url='login')
def end_course(request, pk):
    course = Course.objects.get(id=pk)

    if request.method == 'GET':
        student_list = Students_Course.objects.filter(course=course)
        for student in student_list:
            if str(student.status) == str("Completed"):
                messages.info(request, 'This class is already ended')
                return redirect('course_grades', request.user.faculty.id)

            elif student.grade is None:
                messages.info(request, student.student.name + 'does not have a grade. All students must have a grade '
                                                              'before you can end the course')
                return redirect('course_grades', request.user.faculty.id)

            else:
                student.status = "Completed"
                messages.info(request, 'You have successfully ended ' + course.course_id)
                student.save()

        return redirect('course_grades', request.user.faculty.id)

    context = {'course': course}
    return render(request, 'school/course/end_course.html', context)


'''_____________________________ Course STATISTICS view _________________________________'''


@login_required(login_url='login')
def course_statistics(request, pk):
    course = Course.objects.get(id=pk)
    student_list = Students_Course.objects.filter(course=course)
    grades = list(student_list.values("grade"))
    print("GRADES: ", grades)
    average_digit_grade = grade_converter(grades)
    if len(grades) != 0:
        average_letter_grade = grade_digit_to_letter(average_digit_grade)
    else:
        average_letter_grade = None

    num_passing_grade = student_list.exclude(grade="F").exclude(grade=None).count()
    num_of_students = course.capacity - course.seats_open

    grade_A = student_list.filter(grade="A").count() / num_of_students * 100 \
        if num_of_students != 0 else 0
    grade_B = student_list.filter(grade="B").count() / num_of_students * 100 \
        if num_of_students != 0 else 0
    grade_C = student_list.filter(grade="C").count() / num_of_students * 100 \
        if num_of_students != 0 else 0
    grade_D = student_list.filter(grade="D").count() / num_of_students * 100 \
        if num_of_students != 0 else 0
    grade_F = student_list.filter(grade="F").count() / num_of_students * 100 \
        if num_of_students != 0 else 0

    context = {'course': course,
               'num_passing_grade': num_passing_grade,
               'average_letter_grade': average_letter_grade,
               'grade_A': grade_A,
               'grade_B': grade_B,
               'grade_C': grade_C,
               'grade_D': grade_D,
               'grade_F': grade_F}
    return render(request, 'school/course/course_statistics.html', context)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             GRADE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

'''_____________________________ Course Grade view _________________________________'''


@login_required(login_url='login')
def course_grades(request, pk):
    user = request.user

    if user.is_faculty:
        faculty = user.faculty
        courses = faculty.course_set.all()

        student_course_dic = {}
        for course in courses:
            student_list = Students_Course.objects.filter(course=course)
            student_course_dic[course] = student_list
            context = {
                'student_course_dic': student_course_dic
            }

        return render(request, 'school/faculty/course_grades.html', context)

    elif user.is_student:
        student = user.student
        student_course_query = Students_Course.objects.filter(student=student)

        course_list_query = list(student_course_query.values("course"))
        course_list = [Course.objects.get(id=item["course"]) for item in course_list_query]
        grade_list = [item["grade"] for item in list(student_course_query.values("grade"))]

        context = {
            'grade_dict': dict(zip(course_list, grade_list))
        }

        return render(request, 'school/student/grades.html', context)


'''_____________________________ UPDATE Grade view _________________________________'''


def update_grade(request, pk):
    form = GradeForm()
    if request.method == 'POST':  # It doesn't access this condition so the updates won't occur
        student_course = Students_Course.objects.get(id=pk)
        form = GradeForm(request.POST, instance=student_course)
        if form.is_valid():
            form.save()
            return redirect('course_grades', request.user.faculty.id)

    context = {
        'form': form,
    }
    return render(request, 'school/course/update_grade.html', context)


def grade_digit_to_letter(grade):
    if grade >= 3.5:
        return "A"
    if grade >= 2.5:
        return "B"
    if grade >= 1.5:
        return "C"
    if grade >= 0.5:
        return "D"
    else:
        return "F"


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


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
New Section:                             PDF Report
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def get_student_data(request, pk):
    student = Student.objects.get(id=pk)
    completed_courses = student.students_course_set.filter(status="Completed")
    student_grades = list(completed_courses.values("grade"))

    student_gpa = grade_converter(student_grades)
    data = {
        "name": student.name,

        "date_of_birth": student.date_of_birth,
        "address": student.address,
        "phone": request.user.phone_number,
        "email": student.email,

        "major": student.major,
        "minor": student.minor,
        "graduate_student": student.graduate_student,

        "completed_courses": completed_courses,
        "student_gpa": student_gpa,
    }
    return data


# Opens up page as PDF
class student_report_pdf(View):
    def get(self, request, pk, *args, **kwargs):

        pdf = render_to_pdf('school/student_report_pdf.html', get_student_data(request, pk))
        return HttpResponse(pdf, content_type='application/pdf')


def get_grade_sheet_data(request, pk):
    course = Course.objects.get(id=pk)
    student_list = Students_Course.objects.filter(course=course)

    data = {
        'course': course,
        'student_list': student_list,
        'total_students': len(student_list),
    }

    return data


# Opens up page as PDF
class grade_sheet_pdf(View):
    def get(self, request, pk, *args, **kwargs):
        data = get_grade_sheet_data(request, pk)
        pdf = render_to_pdf('school/grade_sheet_pdf.html', get_grade_sheet_data(request, pk))

        return HttpResponse(pdf, content_type='application/pdf' )
