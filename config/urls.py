"""f2kens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
#Import views from f2kens app
from f2kens.views import *
from frontend_token.views import *

#TODO: Testear urls
#TODO: Documentar
#TODO: Agregar parametros a urls
#TODO: Mover a Django 2

#URLS
urlpatterns = [

    #Django admin
    path('admin/', admin.site.urls),

    #Indexes
    path('i-Preceptor/', indexPreceptor, name='index_preceptor'),
    path('c-F2/', createF2, name='create_F2'),
    path('state/<int:form2_id>/<int:mod>', checkForm, name='verificarXD')
]
