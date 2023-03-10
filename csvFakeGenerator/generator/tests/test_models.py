from django.test import TestCase

from ..models import DataSchema, Column


class DataSchemaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='root', password='1234')
        data_schema = DataSchema.objects.create(name='Simple schema', column_separator='`', string_character='|')
        column_1 = Column.objects.create(name='Name', data_type='FULL_NAME', order=1, data_schema = data_schema)
        column_2 = Column.objects.create(name='Age', data_type='INTEGER', order=2, data_schema = data_schema, range_min=1, range_max=5)
        column_3 = Column.objects.create(name='Story', data_type='TEXT', order=3, data_schema = data_schema, range_min=1, range_max=3)
        column_4 = Column.objects.create(name='Name', data_type='EMAIL', order=4, data_schema = data_schema)
        column_5 = Column.objects.create(name='Name', data_type='COMPANY_NAME', order=5, data_schema = data_schema)
        

    def test_title_max_length(self):
        men = Men.objects.get(pk=1)
        max_length = men._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test_get_absolute_url(self):
        schema = Data_schema.objects.get(pk=1)
        self.assertEquals(data_schema.get_absolute_url(), f'/schema/1/')
