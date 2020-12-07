import django_filters
from django import forms
from django.db.models import F

from django_filters import DateFilter
from .models import *


class CourseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    seats_occupied = django_filters.BooleanFilter(label='Open courses',
                                                  field_name='seats_open',
                                                  lookup_expr='lte',
                                                  method='filter_not_full_courses',
                                                  widget=forms.CheckboxInput)

    def filter_not_full_courses(self, queryset, name, value):
        if value:
            queryset = queryset.exclude(seats_open=0)
        return queryset

    prerequisites = django_filters.BooleanFilter(label='Prerequisites Completed',
                                                 field_name='prerequisites',
                                                 method='filter_only_prerequisites_met',
                                                 widget=forms.CheckboxInput)

    def filter_only_prerequisites_met(self, queryset, name, value):
        if value:
            lookup = '__'.join([name, 'iexact'])

            queryset = queryset.exclude(prerequisites=F('prerequisites')).filter(**{lookup: F('prerequisites')})
        return queryset

    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['instructor', 'students', 'start_date', 'end_date', 'time']


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