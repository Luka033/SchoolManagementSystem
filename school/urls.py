from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),


    path('faculty_home', views.faculty_home, name='faculty_home'),
    path('faculty_course_info/', views.faculty_course_info, name='faculty_course_info'),
    path('faculty/<str:pk>', views.faculty_details, name='faculty_details'),
    path('electronic_student_record/', views.electronic_student_record, name='electronic_student_record'),
    path('student/<str:pk>', views.student_details, name='student_details'),
    path('course_grades/', views.course_grades, name='course_grades'),


    path('student_home/', views.student_home, name='student_home'),
    path('course_registration/', views.course_registration, name='course_registration'),
    path('add_course/<str:pk>', views.add_course, name='add_course'),
    path('drop_course/<str:pk>', views.drop_course, name='drop_course'),


    path('account/', views.account_settings, name='account'),
    path('major_requirements/<str:pk>', views.major_requirements_details, name='major_requirements_details'),
    path('majors/', views.majors, name='majors'),
    path('course/<str:pk>', views.course_details, name='course_details'),


]