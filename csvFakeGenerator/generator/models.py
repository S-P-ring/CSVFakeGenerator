from django.db import models
from django.urls import reverse


class DataSchema(models.Model):
    COLOMN_SEPARATOR = (
        (',', 'Comma'),
        (';', 'Semicolon'),
        ('|', 'Vertical Bar'),
    )

    STRING_CHARACTER = (
        ('"', 'Double Quotes'),
        ("'", 'Single Quotes'),
        ('`', 'Backtick'),
    )

    name = models.CharField(max_length=255)
    column_separator = models.CharField(max_length=1, default=',',
                                        choices=COLOMN_SEPARATOR)
    string_character = models.CharField(max_length=1, default='"',
                                        choices=STRING_CHARACTER)
    time_modified = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('generate_data', args=[self.pk])


class Column(models.Model):
    TYPES = (
        ('FULL_NAME', 'Full Name'),
        ('JOB', 'Job'),
        ('EMAIL', 'Email'),
        ('DOMAIN_NAME', 'Domain Name'),
        ('PHONE_NUMBER', 'Phone Number'),
        ('COMPANY_NAME', 'Company Name'),
        ('TEXT', 'Text'),
        ('INTEGER', 'Integer'),
        ('ADDRESS', 'Address'),
        ('DATE', 'Date'),
    )

    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=20, choices=TYPES)
    order = models.PositiveIntegerField()
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)

    range_min = models.IntegerField(null=True, blank=True)
    range_max = models.IntegerField(null=True, blank=True)

    def is_range_supported(self):
        return self.data_type in ('TEXT', 'INTEGER')


class DataSet(models.Model):
    data_schema = models.ForeignKey('DataSchema', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Not Started')
    file_reference = models.FileField(upload_to='datasets/', blank=True, null=True)

    def __str__(self):
        return f"{self.data_schema} - {self.created_date}"
