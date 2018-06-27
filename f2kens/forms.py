# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from . import apiModel
import datetime

class userForm(forms.Form):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=100)
	email = forms.CharField(max_length=100)


	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password']