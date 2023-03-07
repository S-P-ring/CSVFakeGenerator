from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory

from .models import DataSchema
from .models import Column


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ColumnForm(forms.ModelForm):
    range_min = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'range-field'}))
    range_max = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'range-field'}))

    class Meta:
        model = Column
        fields = ['name', 'data_type', 'order', 'range_min', 'range_max']

    def is_supported_range(self):
        return self.cleaned_data['data_type'] in ['TEXT', 'INTEGER']


class DataSchemaForm(forms.ModelForm):
    class Meta:
        model = DataSchema
        fields = ['name', 'column_separator', 'string_character']

    ColumnFormSet = inlineformset_factory(DataSchema, Column, form=ColumnForm, extra=1)
    columns = ColumnFormSet()


class GenerateDataForm(forms.Form):
    num_records = forms.IntegerField(min_value=1)
