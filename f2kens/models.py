import datetime

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from oauth2_provider import models as tokens

from .utils import apiModel


F2_STATES = [
    ('En Espera','En Espera'),
    ('Aprobado','Aprobado'),
    ('Rechazado','Rechazado')
]

STATUS_CHOICES = {
    '1': "Regular",
    '2': "1ra Reincorp",
    '3': "2da Reincorp",
    '4': "Libre"

}

class ApiYear(apiModel.APIModel):
    _url = 'years/'
    year_number = apiModel.Field(int)
    division = apiModel.Field(str)

    @property
    def students(self):
        return ApiStudent.filter(year=self)

    def __str__(self):
        return "{} {}".format(self.year_number, self.division.upper())


class ApiPreceptor(apiModel.APIModel):
    _url = 'preceptors/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    year = apiModel.Field(ApiYear, is_array=True)
    email = apiModel.Field(str)
    internal_tel = apiModel.Field(int)


class ApiStudent(apiModel.APIModel):
    _url = 'students/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    dni = apiModel.Field(int)
    student_tag = apiModel.Field(int)
    list_number = apiModel.Field(int)
    status = apiModel.Field(str, choices=STATUS_CHOICES)
    year = apiModel.Field(ApiYear)

    def parents(self):
        parents = Parent.filter_model(childs=self)
        for parent in parents:
            yield parent


class ApiParent(apiModel.APIModel):
    _url = 'parents/'
    first_name = apiModel.Field(str)
    last_name = apiModel.Field(str)
    email = apiModel.Field(str)
    childs = apiModel.Field(ApiStudent, is_array=True)


class ApiRegistro(apiModel.APIModel):
    _url = 'registros/'
    year = apiModel.Field(ApiYear)
    preceptor = apiModel.Field(ApiPreceptor)
    date = apiModel.Field(datetime.datetime.strptime, False, "%Y-%m-%d")


class ApiAbsence(apiModel.APIModelSaveable):
    _url = 'absence/'
    origin = apiModel.Field(int)
    justified = apiModel.Field(int)
    percentage = apiModel.Field(float)
    registro = apiModel.Field(ApiRegistro)
    student = apiModel.Field(ApiStudent)


class Preceptor(models.Model, apiModel.ApiModelMixin):
    model=apiModel.ApiField(ApiPreceptor, unique=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{model.last_name}, {model.first_name}".format(model=self.model)


class Parent(models.Model, apiModel.ApiModelMixin):
    model = apiModel.ApiField(ApiParent, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
            

class Device(models.Model):
    parent = models.OneToOneField(Parent, null=True, related_name="device", on_delete=models.CASCADE)
    token = models.CharField(max_length=152, unique=True)
    # brand = models.CharField(max_length=128)
    # deviceId 
    # name
    # manufacturer
    # model
    # systemVersion
    # systemType

class Formulario(models.Model):
    student = apiModel.ApiField(ApiStudent)
    date = models.DateField(auto_now=True)
    time = models.TimeField()
    preceptor = models.ForeignKey(Preceptor, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=300)

    class Meta:
        abstract=True
        verbose_name='Formulario'
        verbose_name_plural='Formularios'
        unique_together = (("student", "date"),)

    def __str__(self):
        return '{stud} {date} {time} {prec}'.format(
            stud=self.student, 
            date=self.date, 
            time=self.time, 
            prec=self.preceptor)


class Formulario2(Formulario):      ###clase formulario 2
    finalized = models.BooleanField(default=False)
    state = models.CharField(
        max_length=50,
        choices=F2_STATES,
        default='En Espera')  ###state para las decicisiones (RECHAZAR, ACEPTAR, EN ESPERA)
    

    class Meta:
        verbose_name = 'F2'
        verbose_name_plural = 'F2es'
        unique_together = ("student", "date")

    def updatable(self):
        return (not self.finalized and self.date==datetime.date.today())

    def save(self, *args, **kwargs):
        if not self.pk:
            newModel = super(Formulario2, self).save(*args, **kwargs)
            fcm_service = settings.FCM_SERVICE
            
            data = {
                'id': self.id,
                'student': {
                    "first_name": self.student.first_name, 
                    "last_name": self.student.last_name,
                    "list_number": self.student.list_number},
                'date': str(self.date),
                'time': self.time,
                'motivo': self.motivo,
                'state': self.state,
                }

            for parent in Parent.filter_model(childs=self.student):
                if (hasattr(parent,"device")):
                    result = fcm_service.notify_single_device(
                        registration_id=parent.device.token, 
                        data_message=data,
                        message_body=f"{data['student']['last_name']},{data['student']['first_name']} se puede retirar a partir de las {data['time']}")
                else:
                    subject = "Su hijo {} puede retirarse temprano".format(self.student.first_name)
                    message = '127.0.0.1:8000/tutor/'
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [x.email for x in ApiParent.filter(childs=self.student)],
                        fail_silently=False)
            return newModel
        return super(Formulario2, self).save(*args, **kwargs)

    def __str__(self):
        basestr = super().__str__()
        return "{name} {old}".format(name=self.Meta.verbose_name, old=basestr)

class Formulario3(Formulario):      ###clase formulario 3

    class Meta:
        verbose_name = 'F3'
        verbose_name_plural = 'F3es'

    def __str__(self):
        basestr = super().__str__()
        return "{name} {old}".format(name=self.Meta.verbose_name, old=basestr)

      
class Guard(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.IntegerField()