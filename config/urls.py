from django.urls import path, include
from django.contrib import admin

from f2kens.views import *
from frontend_token import urls
from frontend_token.views import *

#URLS
urlpatterns = [

    #Django admin
    path('admin/', admin.site.urls),

    path("", include(urls.urlpatterns)),
    #Indexes
    path('create_f2/', create_f2, name='create_f2'),
    path('update_f2_state/form_id_<int:form2_id>/', update_f2_state, name='estado_f2')
]
