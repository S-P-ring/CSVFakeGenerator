from django.test import TestCase

from ..models import DataSchema, Column
from django.urls import reverse

class GenerateDataSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='root', password='1234')
        data_schema = DataSchema.objects.create(name='Simple schema', column_separator='`', string_character='|')
        column_1 = Column.objects.create(name='Name', data_type='FULL_NAME', order=1, data_schema = data_schema)
        column_2 = Column.objects.create(name='Age', data_type='INTEGER', order=2, data_schema = data_schema, range_min=1, range_max=5)
        column_3 = Column.objects.create(name='Story', data_type='TEXT', order=3, data_schema = data_schema, range_min=1, range_max=3)
        column_4 = Column.objects.create(name='Name', data_type='EMAIL', order=4, data_schema = data_schema)
        column_5 = Column.objects.create(name='Name', data_type='COMPANY_NAME', order=5, data_schema = data_schema)

    def test_login(self):
        resp = self.client.post('/login/', {'username': 'root', 'password': '1234'}, format='json')
        self.assertEqual(resp.status_code, 200)
     
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'generator/base.html')

    def test_lists_all_shemas(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['schema_list']) == 1)
