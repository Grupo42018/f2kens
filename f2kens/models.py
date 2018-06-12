# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from . import apiModel
import datetime
# Create your models here.

class Preceptor(models.Model):
    api_id=models.IntegerField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Parent(models.Model):
    api_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Device(models.Model):
    token = models.CharField(max_length=128)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)



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