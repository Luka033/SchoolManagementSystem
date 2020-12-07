from django.test import SimpleTestCase
from django.urls import reverse, resolve
from school.views import *

class TestUrls(SimpleTestCase):

    def test_student_report_pdf_is_resolved(self):
        url = reverse('student_report_pdf', args=['0'])
        self.assertEquals(resolve(url).func.view_class, student_report_pdf)

    def test_grade_sheet_pdf_is_resolved(self):
        url = reverse('grade_sheet_pdf', args=['0'])
        self.assertEquals(resolve(url).func.view_class, grade_sheet_pdf)




    def test_signup_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_student_signup_is_resolved(self):
        url = reverse('student_signup')
        self.assertEquals(resolve(url).func.view_class, StudentSignUpView)

    def test_faculty_signup_is_resolved(self):
        url = reverse('faculty_signup')
        self.assertEquals(resolve(url).func.view_class, FacultySignUpView)




    def test_catalog_faculty_is_resolved(self):
        url = reverse('catalog_faculty')
        self.assertEquals(resolve(url).func, catalog_faculty)

    def test_catalog_course_is_resolved(self):
        url = reverse('catalog_course')
        self.assertEquals(resolve(url).func, catalog_course)

    def test_course_detail_is_resolved(self):
        url = reverse('course_detail', args=['0'])
        self.assertEquals(resolve(url).func, course_details)

    def test_catalog_student_is_resolved(self):
        url = reverse('catalog_student')
        self.assertEquals(resolve(url).func, catalog_student)

    def test_catalog_major_is_resolved(self):
        url = reverse('catalog_major')
        self.assertEquals(resolve(url).func, catalog_major)

    def test_major_requirements_is_resolved(self):
        url = reverse('major_requirement', args=['0'])
        self.assertEquals(resolve(url).func, major_requirement)




    def test_faculty_home_is_resolved(self):
        url = reverse('faculty_home')
        self.assertEquals(resolve(url).func, faculty_home)

    def test_faculty_detail_is_resolved(self):
        url = reverse('faculty_detail', args=['0'])
        self.assertEquals(resolve(url).func, faculty_detail)

    def test_faculty_schedule_is_resolved(self):
        url = reverse('faculty_schedule')
        self.assertEquals(resolve(url).func, faculty_schedule)

    def test_course_grades_is_resolved(self):
        url = reverse('course_grades', args=['0'])
        self.assertEquals(resolve(url).func, course_grades)

    def test_update_grade_is_resolved(self):
        url = reverse('update_grade', args=['0'])
        self.assertEquals(resolve(url).func, update_grade)

    def test_end_course_is_resolved(self):
        url = reverse('end_course', args=['0'])
        self.assertEquals(resolve(url).func, end_course)

    def test_course_statistics_is_resolved(self):
        url = reverse('course_statistics', args=['0'])
        self.assertEquals(resolve(url).func, course_statistics)




    def test_student_home_is_resolved(self):
        url = reverse('student_home')
        self.assertEquals(resolve(url).func, student_home)

    def test_student_detail_is_resolved(self):
        url = reverse('student_detail', args=['0'])
        self.assertEquals(resolve(url).func, student_detail)

    def test_outline_is_resolved(self):
        url = reverse('student_outline', args=['0'])
        self.assertEquals(resolve(url).func, student_outline)

    def test_edit_student_outline_is_resolved(self):
        url = reverse('edit_student_outline', args=['0', '0'])
        self.assertEquals(resolve(url).func, edit_student_outline)

    def test_add_outline_course_is_resolved(self):
        url = reverse('add_outline_course', args=['0', '0'])
        self.assertEquals(resolve(url).func, add_outline_course)

    def test_remove_outline_course_is_resolved(self):
        url = reverse('remove_outline_course', args=['0', '0'])
        self.assertEquals(resolve(url).func, remove_outline_course)

    def test_course_registration_is_resolved(self):
        url = reverse('course_registration')
        self.assertEquals(resolve(url).func, course_registration)

    def test_add_course_is_resolved(self):
        url = reverse('add_course', args=['0'])
        self.assertEquals(resolve(url).func, add_course)

    def test_drop_course_is_resolved(self):
        url = reverse('drop_course', args=['0'])
        self.assertEquals(resolve(url).func, drop_course)

    def test_student_schedule_is_resolved(self):
        url = reverse('student_schedule', args=['0'])
        self.assertEquals(resolve(url).func, student_schedule)

    def test_update_personal_info_is_resolved(self):
        url = reverse('update_personal_info')
        self.assertEquals(resolve(url).func, update_personal_info)













