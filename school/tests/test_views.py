from django.test import TestCase, Client
from django.urls import reverse
from school.models import *
from school.views import grade_converter
from school.views import grade_converter, grade_digit_to_letter
import pytest_django





class TestViewsStudent(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(
            username='student1',
            email='student1@gmail.com',
        )
        self.user.set_password('testpassword')
        self.user.save()

        self.student = Student.objects.create(
            user=self.user,
            name='John Doe',
            date_of_birth=timezone.now(),
        )
        self.student.save()

        self.course = Course.objects.create(
            course_id='CS310',
            schedule_number='2001',
            title='Data Structures',
            time='0800-0930',
            day='MW',
            capacity=10,
            seats_open=10,
            semester='FA20',
            start_date=timezone.now(),
            end_date=timezone.now()
        )

        login = self.client.login(username='student1', password='testpassword')
        self.assertEqual(login, True)

        self.catalog_course_url = reverse('catalog_course')
        self.catalog_student_url = reverse('catalog_student')
        self.catalog_faculty_url = reverse('catalog_faculty')
        self.catalog_major_url = reverse('catalog_major')
        self.major_requirements_url = reverse('major_requirement', args=['1'])
        self.update_personal_info_url = reverse('update_personal_info')
        self.student_home_url = reverse('student_home')
        self.student_detail_url = reverse('student_detail', args=[self.student.id])
        self.student_outline_url = reverse('student_outline', args=[self.student.id])
        self.student_schedule_url = reverse('student_schedule', args=[self.student.id])

        self.course_detail_url = reverse('course_detail', args=[self.course.id])
        self.add_course_url = reverse('add_course', args=[self.course.id])
        self.drop_course_url = reverse('drop_course', args=[self.course.id])
        self.course_statistics_url = reverse('course_statistics', args=[self.course.id])


    def test_grade_digit_to_letter(self):
        assert grade_digit_to_letter(3.9) == 'A'
        assert grade_digit_to_letter(2.5) == 'B'
        assert grade_digit_to_letter(1.6) == 'C'
        assert grade_digit_to_letter(0.0) == 'F'


    def test_grade_converter(self):
        grades = [{'grade': 'B', 'grade': 'A','grade': 'C', 'grade': 'C'}]
        assert grade_converter(grades) == 2.0
        assert not grade_converter(grades) > 2.0
        assert not grade_converter(grades) < 2.0
        grades.append({'grade': 'A'})
        assert grade_converter(grades) == 3.0



    def test_catalog_course_GET(self):
        response = self.client.get(self.catalog_course_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/catalog/course_list.html')

    def test_catalog_student_GET(self):
        response = self.client.get(self.catalog_student_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/catalog/student_list.html')

    def test_catalog_faculty_GET(self):
        response = self.client.get(self.catalog_faculty_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/catalog/faculty_list.html')

    def test_catalog_major_GET(self):
        response = self.client.get(self.catalog_major_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/catalog/major_list.html')

    def test_student_home_GET(self):
        response = self.client.get(self.student_home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/student/home.html')

    def test_student_detail_GET(self):
        response = self.client.get(self.student_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/student/detail.html')

    def test_student_schedule_GET(self):
        response = self.client.get(self.student_schedule_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/student/schedule.html')

    def test_course_detail_GET(self):
        response = self.client.get(self.course_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/course/detail.html')

    def test_add_course_GET(self):
        response = self.client.get(self.add_course_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/course/add_course.html')

    def test_add_course_POST(self):
        self.assertEquals(Course.objects.all().count(), 1)
        Course.objects.create(
            course_id='CS320',
            schedule_number='2002',
            title='Programming Languages',
            time='0800-0930',
            day='MW',
            capacity=10,
            seats_open=10,
            semester='FA20',
            start_date=timezone.now(),
            end_date=timezone.now()
        )
        response = self.client.post(self.add_course_url, {
            'course_id': 'CS320',
            'schedule_number': '2002',
            'title': 'Programming Languages',
            'time': '0800-0930',
            'day': 'MW',
            'capacity': 10,
            'seats_open': 10,
            'semester': 'FA20',
            'start_date': '2020-12-07',
            'end_date': '2020-12-07'

        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Course.objects.all().count(), 2)


    def test_course_statistics_GET(self):
        response = self.client.get(self.course_statistics_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/course/course_statistics.html')








class TestViewsFaculty(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(
            username='faculty1',
            email='faculty1@gmail.com',
        )
        self.user.set_password('testpassword')
        self.user.save()

        self.faculty = Faculty.objects.create(
            user=self.user,
            name='Peter Piper',
            date_of_birth=timezone.now(),
            title='Professor',
            office_phone='12345',
            office_number='123',
            office_hours='None'
        )
        self.faculty.save()

        login = self.client.login(username='faculty1', password='testpassword')
        self.assertEqual(login, True)

        self.faculty_home_url = reverse('faculty_home')
        self.faculty_detail_url = reverse('faculty_detail', args=[self.faculty.id])
        self.faculty_schedule_url = reverse('faculty_schedule')

    def test_faculty_home_GET(self):
        response = self.client.get(self.faculty_home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/faculty/home.html')

    def test_faculty_detail_GET(self):
        response = self.client.get(self.faculty_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/faculty/detail.html')

    def test_faculty_schedule_GET(self):
        response = self.client.get(self.faculty_schedule_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/faculty/schedule.html')










