from django.urls import path
from django.contrib import admin

from frontend_token.views import *

urlpatterns = [
    path('', index, name='frontend_index'),
    path('main_preceptor/', index_preceptor, name='index_preceptor'),
    path('get_f2/', get_forms2, name='get_f2')
]