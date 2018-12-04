from django.shortcuts import render, redirect
from django.contrib.auth.decorators import *
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from oauthlib.common import generate_token

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

@decorators.checkGroup("Directives")
def index_director(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dni = request.POST['dni']
        email = request.POST['email']
        passw = generate_token()

        users = User.objects.filter(username__iregex=r"^{}.{}".format(last_name.split(" ")[0], first_name.split(" ")[0]))

        if not users.first():
            username = "{}.{}".format(last_name.split(" ")[0], first_name.split(" ")[0])
        else:
            users = User.objects.filter(username__iregex=r"^{}.{}".format(last_name.split(" ")[0], first_name.split(" ")[0])).order_by('username')
            usplit = users.last().username.split('-')
            last = 0 if len(usplit)==1 else int(usplit[1])
            username = "{}.{}-{}".format(last_name.split(" ")[0], first_name.split(" ")[0], last+1)

        new = User.objects.create(
            username=username, 
            password=passw,
            email=email,
            first_name=first_name,
            last_name=last_name)

        Guard.objects.create(user=new, dni=dni)

        subject = "Su cuenta de f2kens sido creada"
        message = "Para entrar utilice las siguientes credenciales: \n\tUsuario: {}\n\tContrasena: {}".format(username, passw)
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False)

        Group.objects.get(name="Guards").user_set.add(new)

    return render(request, 'director.html', {"guards": Guard.objects.all()})

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