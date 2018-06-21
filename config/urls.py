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
from django.urls import path, include
from django.contrib import admin

from f2kens.views import *
from frontend_token import urls
from frontend_token.views import *

#URLS
urlpatterns = [

    #Django admin
    path('admin/', admin.site.urls),

    #Index
    path('i-Director', renderIndexDirector, name="index_director"),

    #director
    path('modal_preceptor/', modalpre, name="modalpre"),

    path("", include(urls.urlpatterns)),
    #Indexes
    path('create_f2/', create_f2, name='create_f2'),
    path('update_f2_state/form_id_<int:form2_id>/', update_f2_state, name='estado_f2')
]
