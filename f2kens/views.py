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
from .utils import token as token_utils
from utils import decorators

@login_required
@decorators.checkGroup("Preceptors")
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

    try:
        
        for student in students:
            new_F2 = Formulario2(student=student, time=time, preceptor=preceptor, motivo=motive)
            new_F2.save() # Save the F2 object
    except Exception as e:
        return redirect('index_preceptor')
    return redirect('index_preceptor')

@login_required
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


@login_required
@decorators.checkGroup("Tutors")
def update_f2_state(request, form2_id):
    valid_fields = ('Aprobado', 'Rechazado')
    parent = Parent.objects.get(user=request.user)
    form = Formulario2.objects.get(id=form2_id)
    state = request.POST['estado']

    if (form.student in parent.model.childs 
       and state in valid_fields
       and form.updatable()):
        form.state = state
        form.save()
        return redirect('index_tutor')
    return HttpResponse(status=403)

@login_required
@decorators.checkGroup("Preceptors")
def get_f2s(request):
    query = Formulario2.objects.filter(preceptor__user=request.user, date=datetime.date.today(), finalized=False)

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

    f2s = Formulario2.objects.filter(query, date=timezone.now().today(), finalized=False)

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

def get_parents(request, pk):
    student = ApiStudent.get(id=pk)
    parents = Parent.filter_model(childs=student)
    a = []
    for i in parents:
        a.append({
            "first_name":i.model.first_name,
            "last_name": i.model.last_name,
            "id": i.id
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

@decorators.checkGroup("Guards")
def finishF2(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    f2 = Formulario2.objects.get(id=request.POST["id"])
    f2.finalized = True
    f2.save()

    return redirect("index_guard")

@decorators.checkGroup("Guards")
def unfinishF2(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    f2 = Formulario2.objects.get(id=request.POST["id"])
    f2.finalized = False
    f2.save()

    return redirect("index_guard")


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
        
        token, reftok = token_utils.get_or_create_token(device)

        data = {
            'access_token': token.token,
            'refresh_token': reftok.token
        }

        result = settings.FCM_SERVICE.single_device_data_message(registration_id=device.token, data_message=data)
        print(result)

        return HttpResponse(status=200)

@decorators.checkGroup("Tutors")
@login_required
def revoke_device(request):
    access_tokens = tokensmod.AccessToken.objects.filter(user=request.user)

    for token in access_tokens:
        tokensmod.RefreshToken.objects.get(access_token=token).delete()
        token.delete()

    dev = Device.objects.get(parent__user=request.user)
    dev.parent = None
    dev.save()
    return HttpResponse(status=205)