
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import *
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

from f2kens.models import *

def index_director(request):
	return render(request, 'director.html')

def modalpre(request):
	return render(request, 'modalpre.html')

def index(request):
	return render(request, 'index.html')

def index_preceptor(request):
	context = {}
	context['formularios'] = Formulario2.objects.all().order_by('state')
	context['preceptores'] = Preceptor.objects.all()
	context['students'] = ApiStudent.get_all()
	return render(request, 'preceptor.html', context)

def index_guard(request):
	return render(request, 'guard.html')

def index_tutor(request):
	if request.user.groups.filter(name='Tutors').exists():
		parent = Parent.objects.get(user=request.user)
		for student in parent.model.childs:
			get_forms2 = Formulario2.objects.filter(student=student, date=timezone.now().date())
		return render(request, 'tutor.html', {'formularios2': get_forms2})
	else:
		return redirect('login')

def createUser(request):
    form = userForm()
    return render(request, 'form.html', {'form': form})

def base(request):
    return render(request, 'base.html')


class RegistroUsuario(CreateView):
    model = User
    template_name = "form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('check_user')