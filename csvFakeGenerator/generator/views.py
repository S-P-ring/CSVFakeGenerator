from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.shortcuts import render
from .forms import DataSchemaForm, GenerateDataForm

from .forms import LoginUserForm
from .models import DataSchema

from .csv_generator import generate_csv, prepare_data
from .services import is_ajax, get_schema, create_dataset


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'generator/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log in'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class SchemaList(LoginRequiredMixin, ListView):
    model = DataSchema
    template_name = 'generator/base.html'
    context_object_name = 'schemas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fake CSV'
        return context

    def get_queryset(self):
        return DataSchema.objects.all()


class DeleteSchema(DeleteView):
    model = DataSchema
    template_name = 'generator/schema_confirm_delete.html'
    pk_url_kwarg = 'schema_pk'
    context_object_name = 'schema'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete schema'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ShowSchema(DetailView):
    model = DataSchema
    template_name = 'generator/schema.html'
    pk_url_kwarg = 'schema_pk'
    context_object_name = 'schema'


class CreateDataSchema(View):
    form_class = DataSchemaForm
    template_name = 'generator/create_schema.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data_schema = form.save(commit=False)
            columns_formset = form.ColumnFormSet(request.POST, instance=data_schema)
            if columns_formset.is_valid():
                data_schema.save()
                columns_formset.save()
                return redirect('home')
        else:
            columns_formset = form.ColumnFormSet(request.POST)
        return render(request, self.template_name, {'form': form, 'columns_formset': columns_formset})

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})




class GenerateDataSet(View):
    model = DataSchema
    form_class = GenerateDataForm
    template_name = 'generator/generate_data.html'
    pk_url_kwarg = 'schema_pk'
    context_object_name = 'schema'

    def post(self, request, schema_pk):
        data_schema = get_schema(schema_pk)
        data_set = create_dataset(data_schema)
        num_records = int(request.POST.get('num_records'))
        fields = prepare_data(data_schema)
        data_set.status = 'In progress'
        column_separator = data_set.column_separator
        string_character = data_set.string_character
        generate_csv(fields, num_records, column_separator, string_character)
        if is_ajax(request):
            data = {'status': 'success',
                    'dataset_pk': data_set.pk,
                    'dataset_time_create': data_set.created_date, }
            return JsonResponse(data)
        else:
            return HttpResponse("Form submitted")

    def get(self, request, schema_pk):
        schema = get_object_or_404(DataSchema, pk=schema_pk)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'schema': schema})
