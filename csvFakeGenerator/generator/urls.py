from django.urls import path
from .views import LoginUser, SchemaList, logout_user, CreateDataSchema, ShowSchema, DeleteSchema, GenerateDataSet

urlpatterns = [
    path('', SchemaList.as_view(), name='home'),
    path('schema/<int:schema_pk>/', ShowSchema.as_view(), name='schema'),
    path('schema/<int:schema_pk>/delete', DeleteSchema.as_view(), name='delete_schema'),
    path('create/', CreateDataSchema.as_view(), name='create_schema'),
    path('schema/<int:schema_pk>/generate_data/', GenerateDataSet.as_view(), name='generate_data'),

    #login/logout
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]