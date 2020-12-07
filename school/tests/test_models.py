from django.test import TestCase
from school.models import *



class TestModels(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            department_name='Sciences'
        )






















