import json
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .models import *
from .apiModel import *

def check_user_group_before_login(request):
    '''
    Esta vista busca si el usuario pertenece a un grupo de usuario
    especifico y lo redirecciona a su correspondiente url.
    '''
    if request.user.groups.filter(name='Directors').exists(): return redirect('index_director')
    elif request.user.groups.filter(name='Preceptors').exists(): return redirect('index_preceptor')
    elif request.user.groups.filter(name='Tutors').exists(): return redirect('index_tutor')
    elif request.user.groups.filter(name='Guards').exists(): return redirect('index_guard')
    else:
        redirect('login')

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
    to_users = []
    for student in students:
        new_F2 = Formulario2(student=student, time=time, preceptor=preceptor, motivo=motive)
        new_F2.save() # Save the F2 object
        parents = Parent.filter_model(childs=student)
        for i in parents:
            to_users.append(i.user.email)

    subject = "F2KENS: Nuevo formulario de alumno"
    message = '127.0.0.1:8000/get_f2/'
    from_user = 'f2kens@gmail.com'
    send_mail(
        subject,
        message,
        from_user,
        to_users,
        fail_silently=False
    )
    return redirect('index_preceptor')

def update_f2_state(request, form2_id):
    get_form2 = Formulario2.objects.get(id=form2_id)
    get_state = request.POST['estado']
    if get_state == 'Aceptado':
        get_form2.state = 'Aceptado'
        get_form2.save()
        return HttpResponse('FORMULARIO ACEPTADO')
    elif get_state == 'Rechazado':
        get_form2.state = 'Rechazado'
        get_form2.save()
        return HttpResponse('FORMULARIO RECHAZADO')
    else:
        return HttpResponse('FORMULARIO PUESTO EN ESPERA')


def get_f2s(request):
    if request.user.is_authenticated:
        query = Formulario2.objects.filter(preceptor__user=request.user)
    else:
        query = Formulario2.objects.all()

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