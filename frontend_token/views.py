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
	context['preceptores'] = Preceptor.objects.all()
	context['students'] = ApiStudent.getAll()
	return render(request, 'preceptor.html', context)

def getForms2(request):
	context = {}
	context['formularios2'] = Formulario2.objects.all()
	return render(request, 'stateF2.html', context)