from django.urls import path
from django.contrib import admin

from f2kens.views import *

urlpatterns = [
    path('create_f2/', create_f2, name='create_f2'),
    path('update_f2_state/form_id_<int:form2_id>/', update_f2_state, name='estado_f2'),
    path('get_f2s/', get_f2s, name="get_f2s"),
    path('get_years/', get_years, name="get_years"),
    path('create_parent/',create_parent, name='create_parent')
    ]