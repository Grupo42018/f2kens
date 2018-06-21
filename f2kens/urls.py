from django.urls import path
from django.contrib import admin

from f2kens.views import *

urlpatterns = [
    path('create_f2/', create_f2, name='create_f2'),
    path('update_f2_state/form_id_<int:form2_id>/', update_f2_state, name='estado_f2'),
    path('get_students/', get_students, name="get_students"),
]