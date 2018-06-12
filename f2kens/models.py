# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from . import apiModel
import datetime
# Create your models here.

F2_STATES = [
    ('EnEspera','En Espera'),
    ('Aprobado','Aprobado'),
    ('Rechazado','Rechazado')
]

class Preceptor(models.Model):
    api_id=models.IntegerField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.user)

class Parent(models.Model):
    api_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.user)

class Device(models.Model):
    token = models.CharField(max_length=128)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.parent)

class Formulario(models.Model):
    student = models.IntegerField()
    date = models.DateField(auto_now=True)
    time = models.TimeField()
    preceptor = models.ForeignKey(Preceptor,on_delete=models.DO_NOTHING)

    class Meta:
        abstract=True
        verbose_name='Formulario'
        verbose_name_plural='Formularios'

    def __str__(self):
        return '%s %s %s %s' % (self.student,self.date,self.time,self.preceptor)

class Formulario2(Formulario):
    motivo_docente = models.CharField(max_length=300)
    state = models.CharField(choices=F2_STATES,default='EnEspera')
    
class Formulario3(Formulario):
    motivo_alumno = models.CharField(max_length=300)


class ApiYear(apiModel.ApiModel):
    _url = 'years/'
    year_number = apiModel.Field(int)
    division = apiModel.Field(str)

class ApiPreceptor(apiModel.ApiModel):
    _url = 'preceptors/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    year = apiModel.Field(ApiYear, is_array=True)
    email = apiModel.Field(str)
    internal_tel = apiModel.Field(int)

class ApiStudent(apiModel.ApiModel):
    _url = 'students/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    dni = apiModel.Field(int)
    student_tag = apiModel.Field(int)
    status = apiModel.Field(int)
    year = apiModel.Field(ApiYear)

class ApiParent(apiModel.ApiModel):
    _url = 'parents/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    email = apiModel.Field(str)

class ApiRegistro(apiModel.ApiModel):
    _url = 'registros/'
    year = apiModel.Field(ApiYear)
    preceptor = apiModel.Field(ApiPreceptor)
    date = apiModel.Field(datetime.datetime.strptime, False, "%Y-%m-%d")

class ApiAbsence(apiModel.ApiModelSaveable):
    _url = 'absence/'
    origin = apiModel.Field(int)
    justified = apiModel.Field(int)
    percentage = apiModel.Field(float)
    registro = apiModel.Field(ApiRegistro)
    student = apiModel.Field(ApiStudent)