from django.test import SimpleTestCase
from school.forms import *
from school.models import *


class TestForms(SimpleTestCase):

    def test_student_form(self):
        form = GradeForm(data={
            'grade': 'A'
        })

        self.assertTrue(form.is_valid())

    # def test_course_form(self):
    #     form = CourseForm(data={
    #         'course_id': ''
    #     })
    #     self.assertTrue(form.is_valid())















