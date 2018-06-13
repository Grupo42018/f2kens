from django.urls import path
from django.contrib import admin

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
    path('forms2recibidos/', getForms2, name='recibir_F2'),
    path('forms2recibidos/<int:form2_id>/', updateF2state, name='estado_f2')
]
