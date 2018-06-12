# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from controlAsistencia.models import *
from controlAsistencia.views import *
# Create your views here.

def index(request):
	return render(request, 'login.html')

def renderIndexDirector(request):
	context = {}
	context['preceptores'] = Preceptor.objects.all()
	context['dispositivos'] = Device.objects.all()
	context['directores'] = Director.objects.all()
	context['alumnos'] = Student.objects.all()
	context['asistencias'] = Absence.objects.all()
	context['tutores'] = Tutor.objects.all()
	context['cursos'] = Curso.objects.all()
	context['cursos_auxiliares'] = Curso_aux.objects.all()
	context['formularios2'] = Form2.objects.all()
	context['formularios3'] = Form3.objects.all()
	return render(request, 'test/directorTEST.html', context)

def modalpre(request):
	return render(request, 'modalpre.html')

