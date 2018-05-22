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
from django.conf.urls import url
from django.contrib import admin
#Import views from f2kens app
from f2kens.views import *

#TODO: Testear urls
#TODO: Documentar
#TODO: Agregar parametros a urls
#TODO: Mover a Django 2

#URLS
urlpatterns = [

    #Django admin
    url(r'^admin/', admin.site.urls),

    #Index
    #url(r'^/$', index, name="index"),

    #CUD preceptor
    url(r'^c-Preceptor/', createPreceptor, name="create_preceptor"),
    url(r'^u-Preceptor/', updatePreceptor, name="update_preceptor"),
    url(r'^d-Preceptor/', deletePreceptor, name="delete_preceptor"),

    #CUD tutor
    url(r'^c-Tutor/', createTutor, name="create_tutor"),
    url(r'^u-Tutor/', updateTutor, name="update_tutor"),
    url(r'^d-Tutor/', deleteTutor, name="delete_tutor"),

    #CUD student
    url(r'^c-Student/', createStudent, name="create_student"),
    url(r'^u-Student/', updateStudent, name="update_student"),
    url(r'^d-Student/', deleteStudent, name="delete_student"),

    #CUD F2
    url(r'^c-F2/', createF2, name="create_F2"),
    url(r'^u-F2/', updateF2, name="update_F2"),
    url(r'^d-F2/', deleteF2, name="delete_F2"),

    #CUD F3
    url(r'^c-F3/', createF3, name="create_F3"),
    url(r'^u-F3/', updateF3, name="update_F3"),
    url(r'^d-F3/', deleteF3, name="delete_F3"),

    #CUD course
    url(r'^c-Course/', createCourse, name="create_course"),
    url(r'^u-Course/', updateCourse, name="update_course"),
    url(r'^d-Course/', deleteCourse, name="delete_course"),

    #CUD absence
    url(r'^c-Absence/', createAbsence, name="create_absence"),
    url(r'^u-Absence/', updateAbsence, name="update_absence"),
    url(r'^d-Absence/', deleteAbsence, name="delete_absence"),

    #CUD device
    url(r'^c-Device/', createDevice, name="create_device"),
    url(r'^u-Device/', updateDevice, name="update_device"),
    url(r'^d-Device/', deleteDevice, name="delete_device"),

    #CUD auxiliar course
    url(r'^c-AuxCourse/', createAuxiliarCourse, name="create_auxCourse"),
    url(r'^u-AuxCourse/', updateAuxiliarCourse, name="update_auxCourse"),
    url(r'^d-AuxCourse/', deleteAuxiliarCourse, name="delete_auxCourse")
]
