from django.test import TestCase, Client
from django.urls import reverse
from school.models import *
import json



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.catalog_course_url = reverse('catalog_course')
        self.course_detail_url = reverse('course_detail', args=['0'])
        self.catalog_student_url = reverse('catalog_student')


    def test_catalog_course_GET(self):
        response = self.client.get(self.catalog_course_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/catalog/course_list.html')

    # def test_catalog_student_GET(self):
    #     response = self.client.get(self.catalog_student_url)
    #     self.assertEquals(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'school/catalog/student_list.html')

    # def test_course_detail_GET(self):
    #     response = self.client.get(self.course_detail_url)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'school/course/detail.html')












