# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from . import apiModel
import datetime

F2_STATES = [
    ('EnEspera','En Espera'),
    ('Aprobado','Aprobado'),
    ('Rechazado','Rechazado')
]


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



class Preceptor(models.Model):
    model=apiModel.ApiField(ApiPreceptor, unique=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Parent(models.Model):
    model = apiModel.ApiField(ApiParent, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Device(models.Model):
    token = models.CharField(max_length=128)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)


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
        return '{stud} {date} {time} {prec}'.format(
            stud=self.student, 
            date=self.date, 
            time=self.time, 
            prec=self.preceptor)


class Formulario2(Formulario):      ###clase formulario 2
    motivo_docente = models.CharField(max_length=300)
    state = models.CharField(
        max_length=50,
        choices=F2_STATES,
        default='EnEspera')  ###state para las decicisiones (RECHAZAR, ACEPTAR, EN ESPERA)
    
    class Meta:
        verbose_name = 'F2'
        verbose_name_plural = 'F2es'

    def __str__(self):
        basestr = super().__str__()
        return "{name} {old}".format(name=self.Meta.verbose_name, old=basestr)


class Formulario3(Formulario):      ###clase formulario 3
    motivo_alumno = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'F3'
        verbose_name_plural = 'F3es'

    def __str__(self):
        basestr = super().__str__()
        return "{name} {old}".format(name=self.Meta.verbose_name, old=basestr)

