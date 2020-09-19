from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('faculty/', views.faculty, name='faculty'),
    path('student/<str:pk>', views.student, name='student'),

    path('major_requirements/', views.major_course_requirements),

    path('create_course/', views.create_course, name='create_course'),
    path('update_course/<str:pk>', views.update_course, name='update_course'),
    path('delete_course/<str:pk>', views.delete_course, name='delete_course'),

    path('create_student/', views.create_student, name='create_student'),
    path('update_student/<str:pk>', views.update_student, name='update_student'),
    path('delete_student/<str:pk>', views.delete_student, name='delete_student'),

    path('course_registration/', views.course_registration, name='course_registration'),
]