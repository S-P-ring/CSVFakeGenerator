from django.shortcuts import get_object_or_404

from .models import DataSet, DataSchema


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_schema(pk):
    return get_object_or_404(DataSchema, pk=pk)

def create_dataset(data_schema):
    return DataSet.objects.create(data_schema=data_schema)

def get_ajax_data_response(data_set):
    data = {
            'status': 'success',
            'dataset_pk': data_set.pk,
            'dataset_time_create': data_set.created_date, }
    return data    

def generate_data(*, schema_pk, data_set, num_records):
        data_schema = get_schema(schema_pk)
        fields = prepare_data(data_schema)
        data_set.status = 'In progress'
        column_separator = data_set.column_separator
        string_character = data_set.string_character
        generate_csv(fields, num_records, column_separator, string_character)
        
 def get_num_records(request):
     retunr int(request.POST.get('num_records'))
