from django.urls import path, include
from django.contrib import admin

from f2kens.views import *
from frontend_token import urls
from frontend_token.views import *
#TODO: Testear urls
#TODO: Documentar
#TODO: Agregar parametros a urls
#TODO: Mover a Django 2

#URLS
urlpatterns = [

    #Django admin
    path('admin/', admin.site.urls),

    path("", include(urls.urlpatterns)),
    #Indexes
    path('c-F2/', createF2, name='create_F2'),
    path('forms2recibidos/<int:form2_id>/', updateF2state, name='estado_f2')
]
