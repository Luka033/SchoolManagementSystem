import django_filters
from django import forms
from django_filters import DateFilter
from .models import *
from django.db.models import F
from django.db.models import Q


class CourseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    seats_occupied = django_filters.BooleanFilter(label='Show only open course',
                                                  field_name='seats_occupied',
                                                  method='filter_not_full_courses',
                                                  widget=forms.CheckboxInput)

    def filter_not_full_courses(self, queryset, name, value):
        if value:
            lookup = '__'.join([name, 'lt'])
            queryset = queryset.exclude(seats_occupied=F('seats_available')).filter(**{lookup: F('seats_available')})
        return queryset

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