from django.urls import path
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from f2kens.views import *

urlpatterns = [
    path('', lambda x:HttpResponse(status=200), name="HEAD"),
    path('create_f2/', create_f2, name='create_f2'),
    path('update_f2_state/form_id_<int:form2_id>/', csrf_exempt(update_f2_state), name='estado_f2'),
    path('get_f2s/', get_f2s, name="get_f2s"),
    path('f2s/', get_childs_f2s, name="get_childs_f2s"),
    path('f2/<int:pk>', get_f2, name='f2'),
    path('get_years/', get_years, name="get_years"),
    path('get_parents/<int:pk>', get_parents, name="get_parents"),
    path('reg_device/', csrf_exempt(register_device), name="reg_device"),
    path('lnk_device/', LinkDevice.as_view(), name="lnk_device"),
    path('rvk_device/', revoke_device, name="rvk_device"),
    path('finishF2/', finishF2, name="finishF2"),
    path('unfinishF2/', unfinishF2, name="unfinishF2"),
    ]