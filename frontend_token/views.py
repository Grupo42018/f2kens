from django.shortcuts import render, redirect
from django.contrib.auth.decorators import *
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

from f2kens.models import *
from utils import decorators


def select_user_group(request):
    query_set = Group.objects.filter(user=request.user)

    return render(request, 'user_group.html', {'user_groups':query_set})

@login_required
def check_user_group_before_login(request):
    '''
    Esta vista busca si el usuario pertenece a un grupo de usuario
    especifico y lo redirecciona a su correspondiente url.
    '''
    redirects = {
        'Directives': redirect('index_director'),
        'Preceptors': redirect('index_preceptor'),
        'Tutors': redirect('index_tutor'),
        'Guards': redirect('index_guard')
    }

    if request.user.groups.all().count() > 1:
        return select_user_group(request)
    
    red = redirects.get(request.user.groups.first().name, redirect('login'))
    return red

def index_director(request):
    return render(request, 'director.html')

def modalpre(request):
    return render(request, 'modalpre.html')

def index(request):
    return render(request, 'index.html')

@decorators.checkGroup("Preceptors")
def index_preceptor(request):
    context = {
        'formularios': Formulario2.objects.filter(preceptor__user=request.user),
        'years': Preceptor.objects.get(user=request.user).model.year,
        'all_approved_f2': Formulario2.objects.filter(
            preceptor__user=request.user,
            date=timezone.now().today(),
            state='Aprobado'
        ),
        'all_rejected_f2': Formulario2.objects.filter(
            preceptor__user=request.user,
            date=timezone.now().today(),
            state='Rechazado'
        ),
        'all_on_hold_f2': Formulario2.objects.filter(
            preceptor__user=request.user,
            date=timezone.now().today(),
            state='En Espera'
        )
    }

    return render(request, 'preceptor.html', context)

@decorators.checkGroup("Guards")
def index_guard(request):
    return render(request, 'guard.html', {"exits":Formulario2.objects.filter(state="Aprobado", date=timezone.now().today())})

@decorators.checkGroup("Tutors")
def index_tutor(request):
    get_forms2=[]
    parent = Parent.objects.get(user=request.user)
    for student in parent.model.childs:
        get_forms2.append(Formulario2.objects.filter(student=student, date=timezone.now().today(), finalized=False))
    return render(request, 'tutor.html', {'formularios2': get_forms2, 'parent':parent})

@login_required
def profile(request):
    if request.method == "POST":
        if (request.user.check_password(request.POST['passwordOld'])): 
            if request.POST['passwordNew'] == request.POST['passwordRep']:
                request.user.set_password(request.POST['passwordNew'])
                request.user.save()
                return redirect('profile')
            else:
                return render(request, 'profile.html', {'error': "Las nuevas contrasenas no coinciden"})
        else:
            return render(request, 'profile.html', {'error': "La contrasena original es incorrecta"})
    return render(request, "profile.html")