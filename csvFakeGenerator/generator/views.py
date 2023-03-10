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
from .services import is_ajax, create_dataset, get_ajax_data_response, get_num_records, generate_data


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
    """
        Home page of the site.
        Displays a list of all DataSchema objects.
    """
    model = DataSchema
    template_name = 'generator/base.html'
    context_object_name = 'schemas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fake CSV'
        return context

    def get_queryset(self):
        return DataSchema.objects.all()


class DeleteSchema(LoginRequiredMixin, DeleteView):
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


def logout_user(LoginRequiredMixin, request):
    logout(request)
    return redirect('login')


class ShowSchema(LoginRequiredMixin, DetailView):
    """Displays a shema with a defined pk"""
    model = DataSchema
    template_name = 'generator/schema.html'
    pk_url_kwarg = 'schema_pk'
    context_object_name = 'schema'


class CreateDataSchema(LoginRequiredMixin, View):
    """
        Form of creation DataSchema.
        Column_form_set is used to display a form,
        for creating Column objects on the same page at the same time
    """
    
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




class GenerateDataSet(LoginRequiredMixin, View):
    """
        The generate_data function generates the data.
        It uses an ajax request that checks if the file is ready.
        When ready it returns success.
    """
    model = DataSchema
    form_class = GenerateDataForm
    template_name = 'generator/generate_data.html'
    pk_url_kwarg = 'schema_pk'
    context_object_name = 'schema'

    def post(self, request, schema_pk):
        data_set = create_dataset(data_schema)
        num_records = get_num_records(request)
        generate_data(schema_pk=schema_pk, data_set=data_set, num_records=num_records)
        if is_ajax(request):
            data = get_ajax_data_response(data_set)
            return JsonResponse(data)
        else:
            return HttpResponse("Form submitted")

    def get(self, request, schema_pk):
        schema = get_object_or_404(DataSchema, pk=schema_pk)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'schema': schema})
