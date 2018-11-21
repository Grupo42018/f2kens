from django.apps import AppConfig
from django.conf import settings
class F2KensConfig(AppConfig):
    name = 'f2kens'

    def ready(self):
        import pyfcm
        from django.contrib.auth.models import Group
        from oauth2_provider import models as oauth2models
        tutors, created = Group.objects.get_or_create(name='Tutors')
        directives, created = Group.objects.get_or_create(name='Directives')
        guards, created = Group.objects.get_or_create(name='Guards')
        preceptors, created = Group.objects.get_or_create(name='Preceptors')

        app, created = oauth2models.Application.objects.get_or_create(
            name="Parents", 
            client_type=oauth2models.Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=oauth2models.Application.GRANT_AUTHORIZATION_CODE)

        settings.F2KENS_APPLICATION = app

        settings.FCM_SERVICE = pyfcm.FCMNotification(settings.FCM_SETTINGS['api'])