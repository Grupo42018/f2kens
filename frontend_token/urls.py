from django.urls import path
from django.contrib import admin
from frontend_token.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('bye/', auth_views.logout, name='logout'),
    path('main_preceptor/', index_preceptor, name='index_preceptor'),
    path('get_f2/', get_forms2, name='get_f2')
]