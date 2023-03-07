from django.shortcuts import get_object_or_404

from .models import DataSet, DataSchema


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_schema(pk):
    return get_object_or_404(DataSchema, pk=pk)

def create_dataset(data_schema):
    return DataSet.objects.create(data_schema=data_schema)
