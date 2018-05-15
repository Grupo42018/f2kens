# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from controlAsistencia import models, views
# Create your views here.

def createPreceptor(request):
    firstname = request.POST['preceptor_firstname']
    lastname = request.POST['preceptor_lastname']
    schedule = request.POST['preceptor_schedule']
    try:
        new_preceptor = Preceptor(firstname=firstname, lastname=lastname, schedule=schedule)
        new_preceptor.save()
        #HttpResponse solo para testear
        return HttpResponse("Preceptor creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear el preceptor")

def deletePreceptor(request, preceptor_id):
    try:
        get_preceptor = Preceptor.objects.get(id=preceptor_id)          
        get_preceptor.delete()
        #HttpResponse solo para testear
        return HttpResponse("Preceptor eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el preceptor")
    
def createTutor(request):
    firstname = request.POST['tutor_firstname']
    lastname = request.POST['tutor_lastname']
    phone = request.POST['tutor_phone']
    email = request.POST['tutor_email']
    try:
        device = Device.objects.get(id=request.POST['tutor_device'])
        new_tutor = Tutor(firstname=firstname, lastname=lastname, phone=phone, email=email)
        new_tutor.save()
        #HttpResponse solo para testear
        return HttpResponse("Tutor creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear tutor")

def deleteTutor(request, tutor_id):
    try:
        get_tutor = Tutor.objects.get(id=tutor_id)          
        get_tutor.delete()
        #HttpResponse solo para testear
        return HttpResponse("Tutor eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el Tutor")

def createStudent(request):
    pass

def deleteStudent(request, student_id):
    try:
        get_student = Student.objects.get(id=student_id)          
        get_student.delete()
        #HttpResponse solo para testear
        return HttpResponse("Alumno eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el alumno")

def createF2(request):
    schedule = request.POST['f2_schedule']
    #No se necesita date porque se crea automaticamente con la flecha actual
    #date = request.POST['f2_schedule']
    try:
        student = Student.objects.get(id=request.POST['f2_student'])
        preceptor = Preceptor.objects.get(id=request.POST['f2_preceptor'])
        new_f2 = Form2(schedule=schedule, student=student, preceptor=preceptor)
        new_f2.save()
        #HttpResponse solo para testear
        return HttpResponse("F2 creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear el F2")

def deleteF2(request, form2_id):
    try:
        get_f2 = Form2.objects.get(id=form2_id)          
        get_f2.delete()
        #HttpResponse solo para testear
        return HttpResponse("F2 eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el F2")

def createF3(request):
    schedule = request.POST['f3_schedule']
    reason = request.POST['f3_reason']
    #No se necesita date porque se crea automaticamente con la flecha actual
    #date = request.POST['f3_schedule']
    try:
        student = Student.objects.get(id=request.POST['f3_student'])
        preceptor = Preceptor.objects.get(id=request.POST['f3_preceptor'])
        new_f3 = Form3(schedule=schedule, student=student, preceptor=preceptor, reason=reason)
        new_f3.save()
        #HttpResponse solo para testear
        return HttpResponse("F3 creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear el F3")

def deleteF3(request, form3_id):
    try:
        get_f3 = Form3.objects.get(id=form3_id)          
        get_f3.delete()
        #HttpResponse solo para testear
        return HttpResponse("F3 eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el F3")

def createCourse(request):
    year = request.POST['course_year']
    division = request.POST['course_division']
    try:
        add_preceptor = Preceptor.objects.get(id=request.POST['course_preceptor'])
        new_course = Curso(year=year, division=division, preceptores=add_preceptor)
        new_course.save()
        #HttpResponse solo para testear
        return HttpResponse("Curso creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al creado el curso")

def deleteCourse(request, course_id):
    try:
        get_course = Curso.objects.get(id=course_id)          
        get_course.delete()
        #HttpResponse solo para testear
        return HttpResponse("Curso eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el curso")

def createAbsence(request):
    pass

def deleteAbsence(request, abscence_id):
    try:
        get_abscence = Abscence.objects.get(id=abscence_id)          
        get_abscence.delete()
        #HttpResponse solo para testear
        return HttpResponse("Asistencia eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el asistencia")

def createDevice(request):
    #token = request.POST['device_token']
    pass