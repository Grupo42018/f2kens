from django.apps import AppConfig
class F2KensConfig(AppConfig):
    name = 'f2kens'

    def ready(self):
        from django.contrib.auth.models import Group
        tutors, created = Group.objects.get_or_create(name='Tutors')
        directives, created = Group.objects.get_or_create(name='Directives')
        guards, created = Group.objects.get_or_create(name='Guards')
        preceptors, created = Group.objects.get_or_create(name='Preceptors')