import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.contrib.auth.decorators import login_required, permission_required

from .models import *

def create_f2(request):
    '''
    Esta vista se usa para crear F2. Se envia
    notificacion por email al tutor del estudiante.
    '''
    # Get preceptor by logged user
    preceptor = Preceptor.objects.get(user=request.user)
    print(preceptor)#Log in console
    # Temporary solution for preventing the return of Generators
    # Searches One ApiStudent Object filtered by dni
    students = ApiStudent.filter(year=request.POST['year'])  # FIXME
    time = request.POST['time'] # Get data by post
    # Create the Form object
    to_users = []
    for student in students:
        new_F2 = Formulario2(student=student._api_id, time=time, preceptor=preceptor)
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


def get_years(request):
    if request.user.is_authenticated:
        return get_year_loged(request)
    return get_year_unloged(request)


def get_year_unloged(request):
    a = []
    for i in ApiYear.get_all():
        a.append({
            'id': i._api_id,
            'first_name': i.first_name,
            'last_name': i.last_name,
            'year': str(i.year)
            })
    return JsonResponse(a, safe=False)


def get_year_loged(request):
    a = []
    prec = Preceptor.objects.get(user=request.user)
    for i in prec.model.year:
        a.append({
            'id': i._api_id,
            'division': i.division,
            'year_number': i.year_number,
            })
    return JsonResponse(a, safe=False)