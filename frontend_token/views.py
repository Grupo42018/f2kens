from django.shortcuts import render, redirect
from f2kens.models import *

def index(request):
	return render(request, 'preceptor.html')

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