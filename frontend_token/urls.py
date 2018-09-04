from django.urls import path
from django.contrib import admin
from f2kens.views import check_user_group_before_login
from frontend_token.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('checking_user/', check_user_group_before_login, name='check_user'),
    path('preceptor/', index_preceptor, name='index_preceptor'),
    path('director/', index_director, name="index_director"),
    path('tutor/', index_tutor, name='index_tutor'),
    path('guardia/', index_guard, name='index_guardia'),
    path('modal_preceptor/', modalpre, name="modalpre")
]