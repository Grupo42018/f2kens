import json
import datetime

import pyfcm
from django.apps import apps
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import *
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from oauth2_provider import models as tokensmod
from oauth2_provider.views.mixins import OAuthLibMixin
from oauthlib.common import generate_token

from .models import *
from .utils.apiModel import *
from .utils import mixins
from utils import decorators

# TODO: Actualizar documentación de las vistas.

def select_user_group(request):
	if request.user.is_authenticated:
		#query_set = User.objects.filter(username=request.user, groups__name__in=Group.objects.all())
		query_set = Group.objects.filter(user=request.user)
	else:
		return redirect('login')
	return render(request, 'user_group.html', {'user_groups':query_set})

def check_user_group_before_login(request):
    '''
    Esta vista busca si el usuario pertenece a un grupo de usuario
    especifico y lo redirecciona a su correspondiente url.
    '''
    if request.user.groups.all().count() > 1:
        return select_user_group(request)
    elif request.user.groups.filter(name='Directives'):
        return redirect('index_director')
    elif request.user.groups.filter(name='Preceptors'):
        return redirect('index_preceptor')
    elif request.user.groups.filter(name='Tutors'):
        return redirect('index_tutor')
    elif request.user.groups.filter(name='Guards'):
        return redirect('index_guard')
    else:
        return redirect('login')

@decorators.checkGroup("Preceptors")
@login_required
def create_f2(request):
    '''
    Esta vista se usa para crear F2. Se envia
    notificacion por email al tutor del estudiante.
    '''
    # Get preceptor by logged user
    preceptor = Preceptor.objects.get(user=request.user)
    # Temporary solution for preventing the return of Generators
    # Searches One ApiStudent Object filtered by dni
    students = ApiStudent.filter(year=request.POST['year'])  # FIXME
    time = request.POST['time'] # Get data by post
    motive = request.POST['reason']
    # Create the Form object

    for student in students:
        new_F2 = Formulario2(student=student, time=time, preceptor=preceptor, motivo=motive)
        new_F2.save() # Save the F2 object

    return redirect('index_preceptor')

@decorators.checkGroup("Preceptors")
def get_years(request):
    query = None
    if request.user.is_authenticated:
        query = Preceptor.objects.get(user=request.user).model.year
    else:
        query = ApiYear.get_all()
        
    a=[]
    for i in query:
        a.append({
            'id': i._api_id,
            'division': i.division,
            'year_number': i.year_number,
            })
    return JsonResponse(a, safe=False)


@decorators.checkGroup("Tutors")
@login_required
def update_f2_state(request, form2_id):
    get_form2 = Formulario2.objects.get(id=form2_id)
    get_state = request.POST['estado']
    if get_state == 'Aprobado':
        get_form2.state = 'Aprobado'
        get_form2.save()
    elif get_state == 'Rechazado':
        get_form2.state = 'Rechazado'
        get_form2.save()
    return redirect('index_tutor')

@decorators.checkGroup("Preceptors")
@login_required
def get_f2s(request):
    query = Formulario2.objects.filter(preceptor__user=request.user)

    a=[]
    for i in query:
        a.append({
            'id': i.id,
            'student': {
                "first_name": i.student.first_name, 
                "last_name": i.student.last_name,
                "list_number": i.student.list_number},
            'date': i.date,
            'time': i.time,
            'motivo': i.motivo,
            'state': i.state,
            })
    return JsonResponse(a, safe=False)

@decorators.checkGroup("Tutors")
@login_required
def get_childs_f2s(request):
    childs = Parent.objects.filter(user=request.user).first().model.childs

    query = None

    for student in childs:
        query = Q(student=student) if not query else query | Q(student=student)

    f2s = Formulario2.objects.filter(query, date=timezone.now().today())

    a=[]
    for i in f2s:
        a.append({
            'id': i.id,
            'student': {
                "first_name": i.student.first_name, 
                "last_name": i.student.last_name,
                "list_number": i.student.list_number},
            'date': i.date,
            'time': i.time,
            'motivo': i.motivo,
            'state': i.state,
            })
    return JsonResponse(a, safe=False)

@login_required
def get_f2(request, pk):
    i = Formulario2.objects.get(id=pk)

    a = {
        'id': i.id,
        'student': {
            "first_name": i.student.first_name, 
            "last_name": i.student.last_name,
            "list_number": i.student.list_number},
        'date': i.date,
        'time': i.time,
        'motivo': i.motivo,
        'state': i.state,
        }

    return JsonResponse(a)

def register_device(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    device, created = Device.objects.get_or_create(token=request.POST['token'])

    return JsonResponse({
        'status': 1,
        'device': device.id
        })


class LinkDevice(View, OAuthLibMixin):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LinkDevice, self).dispatch(request, *args, **kwargs)
    
    def post(self, request):
        device = Device.objects.get(id=request.POST.get("device"))
        device.parent = Parent.objects.get(id=request.POST.get('parent'))
        device.save()


        
        tok = generate_token()
        token, created = tokensmod.AccessToken.objects.get_or_create(
            user=device.parent.user,
            application=settings.F2KENS_APPLICATION,
            expires=datetime.date(
                year=datetime.date.today().year,
                month=12,
                day=20),
            token=tok)


        reftok = generate_token()
        tokensmod.RefreshToken.objects.get_or_create(
            user=device.parent.user,
            application=settings.F2KENS_APPLICATION,
            token=reftok,
            access_token=token)

        data = {
            'access_token': tok,
            'refresh_token': reftok
        }

        fcm_service = settings.FCM_SERVICE
        result = fcm_service.single_device_data_message(registration_id=device.token, data_message=data)
        print(result)

        return HttpResponse(status=200)


