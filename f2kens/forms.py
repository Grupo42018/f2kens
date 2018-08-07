# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from . import apiModel
import datetime

class userForm(forms.Form):

	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password']