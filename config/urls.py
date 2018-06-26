from django.urls import path, include
from django.contrib import admin

from f2kens import urls as backurls
from frontend_token import urls as fronturls

#URLS
urlpatterns = [

    #Django admin
    path('admin/', admin.site.urls),

    #Django oauth
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    #Front end urls
    path('', include(fronturls.urlpatterns)),
    
    #Backend urls
    path('f2kens/', include(backurls.urlpatterns))
]