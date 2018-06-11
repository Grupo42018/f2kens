# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from f2kens.models import *
# Create your views here.

def index(request):
	return render(request, 'index.html')

def indexPreceptor(request):
	context = []
	return render(request, 'preceptor.html', context)