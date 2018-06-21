from django.shortcuts import render, redirect
from f2kens.models import *

# Create your views here.

def index_director(request):
	context = {}
	"""
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
	"""
	return render(request, 'director.html', context)

def modalpre(request):
	return render(request, 'modalpre.html')

def index(request):
	return render(request, 'index.html')

def index_preceptor(request):
	context = {}
	context['formularios'] = Formulario2.objects.all()
	context['preceptores'] = Preceptor.objects.all()
	context['students'] = ApiStudent.get_all()
	return render(request, 'preceptor.html', context)

def get_forms2(request):
	context = {}
	context['formularios2'] = Formulario2.objects.all()
	return render(request, 'stateF2.html', context)
