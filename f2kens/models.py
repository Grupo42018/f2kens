# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from . import apiModel
import datetime
# Create your models here.

# Confirmaciones de Tutor
F2_STATES = [
    ('En Espera','En Espera'),
    ('Aprobado','Aprobado'),
    ('Rechazado','Rechazado')
]

#clase preceptor usuario
class Preceptor(models.Model):
    api_id=models.IntegerField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.user)

#clase tutor usuario
class Parent(models.Model):
    api_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.user)

#clase dispositivo de tutor  
class Device(models.Model):
    token = models.CharField(max_length=128)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.parent)

#clase formulario
class Formulario(models.Model):
    student = models.IntegerField()
    date = models.DateField(auto_now=True)
    time = models.TimeField()
    preceptor = models.ForeignKey(Preceptor)

    class Meta:         ###clase que sirve para cambiar la forma en la que se muestra (Formulario/Formularios)
        abstract=True
        verbose_name='Formulario'
        verbose_name_plural='Formularios'

    def __str__(self):
        return '%s %s %s %s' % (self.student, self.date, self.time, self.preceptor)


class Formulario2(Formulario):      ###clase formulario 2
    motivo_docente = models.CharField(max_lenght = 300)
    state = models.CharField(choices=F2_STATES,default=En Espera)  ###state para las decicisiones (RECHAZAR, ACEPTAR, EN ESPERA)
    
class Formulario3(Formulario):      ###clase formulario 3
    motivo_alumno = models.CharField(max_lenght = 300)

#clase curso y año 
class ApiYear(apiModel.ApiModel):
    _url = 'years/'
    year_number = apiModel.Field(int)
    division = apiModel.Field(str)

#clase api.preceptor 
class ApiPreceptor(apiModel.ApiModel):
    _url = 'preceptors/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    year = apiModel.Field(ApiYear, is_array=True)
    email = apiModel.Field(str)
    internal_tel = apiModel.Field(int)

#clase api.Estudiante 
class ApiStudent(apiModel.ApiModel):
    _url = 'students/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    dni = apiModel.Field(int)
    student_tag = apiModel.Field(int)
    status = apiModel.Field(int)
    year = apiModel.Field(ApiYear)


#clase api.Tutor 
class ApiParent(apiModel.ApiModel):
    _url = 'parents/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    email = apiModel.Field(str)


#clase api.Registro
class ApiRegistro(apiModel.ApiModel):
    _url = 'registros/'
    year = apiModel.Field(ApiYear)
    preceptor = apiModel.Field(ApiPreceptor)
    date = apiModel.Field(datetime.datetime.strptime, False, "%Y-%m-%d")


#clase api.Ausencia
class ApiAbsence(apiModel.ApiModelSaveable):
    _url = 'absence/'
    origin = apiModel.Field(int)
    justified = apiModel.Field(int)
    percentage = apiModel.Field(float)
    registro = apiModel.Field(ApiRegistro)
    student = apiModel.Field(ApiStudent)