import getpass
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
            user, created = User.objects.get_or_create(
                username=parent.email.split("@")[0],
                email=parent.email)

            user.first_name=parent.first_name
            user.last_name=parent.last_name

            tutors.user_set.add(user)
            
            try:
                new = models.Parent.objects.create(model=parent, user=user)
            except:
                pass
              
            if created:
                passw = common.generate_token()
                user.set_password(passw)
                send_init_mail(user.email, user.username, passw)
                del passw
            
            user.save()

        #create or get the parents
        for preceptor in models.ApiPreceptor.get_all():
            user, created = User.objects.get_or_create(
                username=preceptor.email.split("@")[0],
                email=preceptor.email)

            user.first_name=preceptor.first_name
            user.last_name=preceptor.last_name

            preceptors.user_set.add(user)

            try:
                new, created = models.Preceptor.objects.get_or_create(model=preceptor, user=user)
            except Exception as e:
                pass

            if created:
                passw = common.generate_token()
                user.set_password(passw)
                send_init_mail(user.email, user.username, passw)
                del passw
            
            user.save()


        if not User.objects.filter(is_superuser=True).first():
            print("Creando super usuario")
            while True:
                email = input("email: ")
                username = input("nombre de usuario: ")
                print("Los caracteres escritos no se mostraran pero seran leiodos")
                passw = getpass.getpass("contrasena: ")
                try:
                    new = User.objects.create_superuser(email=email, username=username, password=passw)
                    directives.user_set.add(new)
                    break
                except Exception as e:
                    print(e)

def send_init_mail(email, user, pas):
    subject = "Su usuario de f2kens fue creado"
    message = 'Ya puede ingresar a la pagina de notificaciones con:\n\
        \tusuario: {}\n\
        \tcontrasena: {}'.format(user, pas)

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False)