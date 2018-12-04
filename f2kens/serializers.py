import datetime

from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import serializers

from . import models
from .utils import apiModel

class ApiField(serializers.Field):
    default_error_messages = {
        'invalid': _('A valid integer is required.'),
        'not_found': _('No model returned with requested id'),
        'max_string_length': _('String value too large.')
    }
    MAX_STRING_LENGTH = 1000

    def __init__(self, model, **kwargs):
        super(ApiField, self).__init__(**kwargs)
        if issubclass(model, apiModel.APIModel): 
            self.model = model
        else:
            raise(TypeError("The model needs to be a subclass of APIModel"))

    def to_internal_value(self, data):
        if isinstance(data, str) and len(data) > self.MAX_STRING_LENGTH:
            self.fail('max_string_length')

        try:
            data = int(data)
            data = self.model.get(pk=data)
        except (ValueError, TypeError):
            self.fail('invalid')
        except (AttributeError):
            self.fail('not_found')
        return data

    def to_representation(self, value):
        return value._api_id


class YearSerializer(serializers.Serializer):
    year_number = serializers.IntegerField(read_only=True)
    division = serializers.CharField(max_length=1)

class StudentSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dni = serializers.IntegerField()
    student_tag = serializers.CharField()
    list_number = serializers.IntegerField()
    status = serializers.CharField()
    year = YearSerializer()

class F2Serializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = models.Formulario2
        fields = (
            'id', 
            'date', 
            'time', 
            'motivo', 
            'finalized',
            'student')

class ApiParentSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    childs = StudentSerializer(many=True)

class ParentSerializer(serializers.ModelSerializer):
    model = ApiParentSerializer()
    class Meta:
        model = models.Parent
        fields = ('device')

class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guard
        fields = (
            'id',
            'email',
            'firstname',
            'lastname',
            'dni')

class PreceptorSerializer(serializers.Serializer):
    pass

class CreateF2(serializers.Serializer):
    year = ApiField(models.ApiYear)
    time = serializers.TimeField()
    reason = serializers.CharField(max_length=190)

    def validate_time(self, value):
        """
        Verify that the exit time is not early nor too late
        """
        if (value>datetime.time(hour=16)):
            raise serializers.ValidationError("El horario es muy tarde")
        elif(value<datetime.time(hour=8)):
            raise serializers.ValidationError("El horario es muy temprano")
        return(value)

