from django.urls import path
from . import views
from school.views import SignUpView, StudentSignUpView, FacultySignUpView


urlpatterns = [
    path('student_report_pdf/<int:pk>', views.student_report_pdf.as_view(), name="student_report_pdf"),
    path('grade_sheet_pdf/<int:pk>', views.grade_sheet_pdf.as_view(), name="grade_sheet_pdf"),


    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/faculty/', FacultySignUpView.as_view(), name='faculty_signup'),

    path('catalog/faculty_list/', views.catalog_faculty, name='catalog_faculty'),
    path('catalog/course_list/', views.catalog_course, name='catalog_course'),
    path('catalog/course/<int:pk>', views.course_details, name='course_detail'),
    path('catalog/student_list/', views.catalog_student, name='catalog_student'),
    path('catalog/major_list/', views.catalog_major, name='catalog_major'),
    path('catalog/major_requirements/<int:pk>', views.major_requirement, name='major_requirement'),

    path('faculty_home/', views.faculty_home, name='faculty_home'),
    path('faculty/detail/<int:pk>', views.faculty_detail, name='faculty_detail'),
    path('faculty/schedule/', views.faculty_schedule, name='faculty_schedule'),
    path('faculty/course_grades/<int:pk>', views.course_grades, name='course_grades'),
    path('update_grade/<str:pk>', views.update_grade, name='update_grade'),
    path('faculty/end_course/<int:pk>', views.end_course, name='end_course'),
    path('course_statistics/<int:pk>', views.course_statistics, name='course_statistics'),

    path('student_home/', views.student_home, name='student_home'),
    path('student/detail/<int:pk>', views.student_detail, name='student_detail'),
    path('student/course_grades/<int:pk>', views.course_grades, name='course_grades'),
    path('student/outline/<int:pk>', views.student_outline, name='student_outline'),
    path('student/edit_student_outline/<int:pk>/<int:pk2>', views.edit_student_outline, name='edit_student_outline'),
    path('student/add_outline_course/<int:pk>/<int:pk2>', views.add_outline_course, name='add_outline_course'),
    path('student/remove_outline_course/<int:pk>/<int:pk2>', views.remove_outline_course, name='remove_outline_course'),
    path('student/course_registration/', views.course_registration, name='course_registration'),
    path('student/add_course/<int:pk>', views.add_course, name='add_course'),
    path('student/drop_course/<int:pk>', views.drop_course, name='drop_course'),
    path('student/schedule/<int:pk>', views.student_schedule, name='student_schedule'),

    path('update_personal_info/', views.update_personal_info, name='update_personal_info'),
]