<<<<<<< HEAD
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
=======
from django.urls import path, include
>>>>>>> develop
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

    #CUD preceptor
    path('c-Preceptor/', createPreceptor, name="create_preceptor"),
    path('u-Preceptor/<int:preceptor_id>', updatePreceptor, name="update_preceptor"),
    path('d-Preceptor/<int:preceptor_id>', deletePreceptor, name="delete_preceptor"),

    #CUD tutor
    path('c-Tutor/', createTutor, name="create_tutor"),
    path('u-Tutor/<int:tutor_id>', updateTutor, name="update_tutor"),
    path('d-Tutor/<int:tutor_id>', deleteTutor, name="delete_tutor"),

    #CUD student
    path('c-Student/', createStudent, name="create_student"),
    path('u-Student/<int:student_id>', updateStudent, name="update_student"),
    path('d-Student/<int:student_id>', deleteStudent, name="delete_student"),

    #CUD F2
    path('c-F2/', createF2, name="create_F2"),
    path('u-F2/<int:form2_id>', updateF2, name="update_F2"),
    path('d-F2/<int:form2_id>', deleteF2, name="delete_F2"),

    #CUD F3
    path('c-F3/', createF3, name="create_F3"),
    path('u-F3/<int:form3_id>', updateF3, name="update_F3"),
    path('d-F3/<int:form3_id>', deleteF3, name="delete_F3"),

    #CUD course
    path('c-Course/', createCourse, name="create_course"),
    path('u-Course/<int:course_id>', updateCourse, name="update_course"),
    path('d-Course/<int:course_id>', deleteCourse, name="delete_course"),

    #CUD absence
    path('c-Absence/', createAbsence, name="create_absence"),
    path('u-Absence/<int:absence_id>', updateAbsence, name="update_absence"),
    path('d-Absence/<int:absence_id>', deleteAbsence, name="delete_absence"),

    #CUD device
    path('c-Device/', createDevice, name="create_device"),
    path('u-Device/<int:device_id>', updateDevice, name="update_device"),
    path('d-Device/<int:device_id>', deleteDevice, name="delete_device"),

    #CUD auxiliar course
    path('c-AuxCourse/', createAuxiliarCourse, name="create_auxCourse"),
    path('u-AuxCourse/<int:auxCourse_id>', updateAuxiliarCourse, name="update_auxCourse"),
    path('d-AuxCourse/<int:auxCourse_id>', deleteAuxiliarCourse, name="delete_auxCourse"),

    #director
    path('', modalpre, name="modalpre")

    path("", include(urls.urlpatterns)),
    #Indexes
    path('create_f2/', create_f2, name='create_f2'),
    path('update_f2_state/form_id_<int:form2_id>/', update_f2_state, name='estado_f2')
]
