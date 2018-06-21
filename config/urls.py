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

from f2kens import urls as backurls
from frontend_token import urls as fronturls

#URLS
urlpatterns = [

    #Django admin
    path('admin/', admin.site.urls),

    #Front end urls
    path('', include(fronturls.urlpatterns)),
    
    #Backend urls
    path('f2kens/', include(backurls.urlpatterns))
]