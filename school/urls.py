from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('faculty_course_info/', views.faculty_course_info, name='faculty_course_info'),
    path('electronic_student_record/', views.electronic_student_record, name='electronic_student_record'),
    path('course_grades/', views.course_grades, name='course_grades'),

    path('faculty_home', views.faculty_home, name='faculty_home'),
    path('user/', views.user_page, name='user_page'),
    path('account/', views.account_settings, name='account'),
    path('student/<str:pk>', views.student, name='student'),

    path('major_requirements/', views.major_course_requirements),

    path('create_course/', views.create_course, name='create_course'),
    path('update_course/<str:pk>', views.update_course, name='update_course'),
    path('delete_course/<str:pk>', views.delete_course, name='delete_course'),

    path('create_student/', views.create_student, name='create_student'),
    path('update_student/<str:pk>', views.update_student, name='update_student'),
    path('delete_student/<str:pk>', views.delete_student, name='delete_student'),

    path('course_registration/', views.course_registration, name='course_registration'),
    path('add_course/<str:pk>', views.add_course, name='add_course')
]