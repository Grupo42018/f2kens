# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

def createF2(request):
    try:
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
        return redirect('index_preceptor')
    except:
        #Handle errors
        html = "<h3 style='color:red'>ERROR AL CREAR F2</h3><br><a href='{% url 'index_preceptor' %}'>Volver</a>"
        return HttpResponse(html)
