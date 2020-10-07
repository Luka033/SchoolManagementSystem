import django_filters
from django import forms
from django_filters import DateFilter
from .models import *


class CourseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    seats_occupied = django_filters.NumberFilter(field_name='seats_occupied',
                                                 lookup_expr='lt')
    # prerequisites = django_filters.ModelMultipleChoiceFilter(queryset=Course.objects.all())
    # seats_occupied = django_filters.ModelChoiceFilter(field_name='seats_occupied',
    #                                               queryset=Course.objects.filter(seats_occupied__gt=0))


    #
    # filter_overrides = {
    #     models.BooleanField: {
    #         'filter_class': django_filters.BooleanFilter,
    #         'extra': lambda f: {
    #             'widget': forms.CheckboxInput,
    #         },
    #     },
    # }


    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['instructor', 'students',
                   'start_date', 'end_date',
                   'time', 'seats_occupied',
                   'seats_available', 'schedule_number']




class FacultyFilter(django_filters.FilterSet):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user', 'office_hours']


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'notes']