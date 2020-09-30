import django_filters
from django_filters import DateFilter
from .models import *


class CourseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')

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