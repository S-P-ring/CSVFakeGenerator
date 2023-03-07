from django.contrib import admin

from .models import DataSchema, Column, DataSet


class DataSchemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'column_separator', 'string_character')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'data_type', 'order', 'data_schema', 'range_min', 'range_max')


admin.site.register(DataSchema, DataSchemaAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(DataSet)
