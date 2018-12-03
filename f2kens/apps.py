from django.apps import AppConfig
from django.conf import settings
from django.core.mail import send_mail
class F2KensConfig(AppConfig):
    name = 'f2kens'

    def ready(self):
        import sys
        
        import pyfcm
        from django.contrib.auth.models import Group, User
        from oauth2_provider import models as oauth2models
        from oauthlib import common

        from . import models

        if ('makemigrations' in sys.argv or 'migrate' in sys.argv):
            return 
          
        #create the user groups
        tutors, created = Group.objects.get_or_create(name='Tutors')
        directives, created = Group.objects.get_or_create(name='Directives')
        guards, created = Group.objects.get_or_create(name='Guards')
        preceptors, created = Group.objects.get_or_create(name='Preceptors')

        #create the oauth app
        app, created = oauth2models.Application.objects.get_or_create(
            name="Parents", 
            client_type=oauth2models.Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=oauth2models.Application.GRANT_AUTHORIZATION_CODE)
        settings.F2KENS_APPLICATION = app

        #start the Firebase Cloud Messaging service
        settings.FCM_SERVICE = pyfcm.FCMNotification(settings.FCM_SETTINGS['api'])

        #create or get the parents
        for parent in models.ApiParent.get_all():
            user, created = User.objects.get_or_create(username=parent.email)

            tutors.user_set.add(user)
            
            try:
                new = models.Parent.objects.create(model=parent, user=user)
            except:
                pass
              
            if created:
                passw = common.generate_token()
                user.set_password(passw)
                send_init_mail(user.username, passw)
                del passw

        #create or get the parents
        for preceptor in models.ApiPreceptor.get_all():
            user, created = User.objects.get_or_create(username=preceptor.email)

            preceptors.user_set.add(user)

            print(preceptor.first_name)

            try:
                new, created = models.Preceptor.objects.get_or_create(model=preceptor, user=user)
            except Exception as e:
                pass

            if created:
                passw = common.generate_token()
                user.set_password(passw)
                send_init_mail(user.username, passw)
                del passw

def send_init_mail(user, pas):
    subject = "Su usuario de f2kens fue creado"
    message = 'Ya puede ingresar a la pagina de notificaciones con:\n\
        \tusuario: {}\n\
        \tcontrasena: {}'.format(user, pas)
    send_mail(
        subject,
        message,
        [user],
        fail_silently=False)