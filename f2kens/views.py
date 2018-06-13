# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail, send_mass_mail, EmailMessage

"""
def createF2(request):
    '''
    Esta vista se usa para crear F2. Se envia
    notificacion por email al tutor del estudiante.
    '''
    try:
        # Get preceptor by logged user
        preceptor = Preceptor.objects.get(user=request.user)
        print(preceptor)#Log in console
        # Temporary solution for preventing the return of Generators
        # Searches One ApiStudent Object filtered by dni
        student = [x._api_id for x in ApiStudent.filter(dni=request.POST['dni'])][0]
        date = request.POST['date'] # Get data by post
        time = request.POST['time'] # Get data by post
        # Create the Form object
        new_F2 = Formulario2(student=student, date=date, time=time, preceptor=preceptor)
        new_F2.save() # Save the F2 object
        print(new_F2) # Log the created object
        try:
            subject = "Nuevo formulario de alumno"
            message = "<h3 style='color:green'>Un alumno espera su confirmacion para retirarse</h3><br><button>CONFIRMAR</button><button>RECHAZAR</button>"
            from_user = 'javierpugliese2000@gmail.com'
            to_users = ['marianovalle13@gmail.com', 'emilioalvarezgg@gmail.com', 'javierpugliese2000@gmail.com', 'juan.fierrofv@gmail.com']
            send_mail(
                subject,
                message,
                from_user,
                to_users,
                fail_silently=False
            )
        except:
            # Handle errors
            html_mail_error = "<h3 style='color:red'>ERROR AL ENVIAR MAIL</h3><br><a href='{% url 'index_preceptor' %}'>Volver</a>"
            # Render html error page
            return HttpResponse(html_mail_error)
        return redirect('index_preceptor')
    except:
        # Handle errors
        html = "<h3 style='color:red'>ERROR AL CREAR F2</h3><br><a href='{% url 'index_preceptor' %}'>Volver</a>"
        # Render html error page
        return HttpResponse(html)
"""
"""
def createF2(request):
    '''
    Esta vista se usa para crear F2. Se envia
    notificacion por email al tutor del estudiante.
    '''
    # Get preceptor by logged user
    preceptor = Preceptor.objects.get(user=request.user)
    print(preceptor)#Log in console
    # Temporary solution for preventing the return of Generators
    # Searches One ApiStudent Object filtered by dni
    student = [x._api_id for x in ApiStudent.filter(dni=request.POST['dni'])][0]  # FIXME
    date = request.POST['date'] # Get data by post
    time = request.POST['time'] # Get data by post
    # Create the Form object
    new_F2 = Formulario2(student=student, date=date, time=time, preceptor=preceptor)
    new_F2.save() # Save the F2 object
    print(new_F2) # Log the created object
    subject = "F2KENS: Nuevo formulario de alumno"
    message = "<h3 style='color:green'>Un alumno espera su confirmacion para retirarse</h3><br><button>CONFIRMAR</button><button>RECHAZAR</button>"
    from_user = 'f2kens@gmail.com'
    to_users = [
        'marianovalle13@gmail.com',
        'emilioalvarezgg@gmail.com',
        'javierpugliese2000@gmail.com',
        'juan.fierrofv@gmail.com',
        'f2kens@gmail.com',
        'martin_montane_6@hotmail.com',
        'mateosenes@gmail.com'
    ]
    send_mail(
        subject,
        message,
        from_user,
        to_users,
        fail_silently=False
    )
    return redirect('index_preceptor')
"""

# Trying with EmailMessage object
def createF2(request):
    '''
    Esta vista se usa para crear F2. Se envia
    notificacion por email al tutor del estudiante.
    '''
    # Get preceptor by logged user
    preceptor = Preceptor.objects.get(user=request.user)
    print(preceptor)#Log in console
    # Temporary solution for preventing the return of Generators
    # Searches One ApiStudent Object filtered by dni
    student = [x._api_id for x in ApiStudent.filter(dni=request.POST['dni'])][0]  # FIXME
    date = request.POST['date'] # Get data by post
    time = request.POST['time'] # Get data by post
    # Create the Form object
    new_F2 = Formulario2(student=student, date=date, time=time, preceptor=preceptor)
    new_F2.save() # Save the F2 object
    print(new_F2) # Log the created object
    subject = "F2KENS: Nuevo formulario de alumno"
    #message = "<h3 style='color:green'>Un alumno espera su confirmacion para retirarse</h3><br><button>CONFIRMAR</button><button>RECHAZAR</button>"
    message = '127.0.0.1:8000/forms2recibidos/'
    from_user = 'f2kens@gmail.com'
    to_users = [
        'javierpugliese2000@gmail.com',
        'f2kens@gmail.com'
    ]
    send_mail(
        subject,
        message,
        from_user,
        to_users,
        fail_silently=False
    )
    return redirect('index_preceptor')

def updateF2state(request, form2_id):
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