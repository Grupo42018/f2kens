# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from f2kens.models import *
# Create your views here.

def index(request):
	return render(request, 'index.html')

def indexPreceptor(request):
	context = {}
	context['formularios'] = Formulario2.objects.all()
	context['formularios_aceptado'] = Formulario2.objects.filter(state="Aprobado")
	context['formularios_rechazado'] = Formulario2.objects.filter(state="Rechazado")
	context['preceptores'] = Preceptor.objects.all()
	context['students'] = ApiStudent.getAll()
	return render(request, 'preceptor.html', context)