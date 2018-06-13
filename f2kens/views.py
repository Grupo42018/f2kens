from django.shortcuts import render

from . import models


### ===> TAREAS:
#TODO: Testear y documentar las vistas
#TODO: Agregar los correspondientes decoradores de vistas
#TODO: Cambiar los HttpResponse por render o redirect
#TODO: Ordenar codigo (clean code)

#Funcion de Crear Preceptor
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


#Funcion de Actualizar Preceptor
def updatePreceptor(request, preceptor_id):
    firstname = request.POST['toUpdate_preceptor_firstname']
    lastname = request.POST['toUpdate_preceptor_lastname']
    schedule = request.POST['toUpdate_preceptor_schedule']
    try:
        toUpdate_preceptor = Preceptor(
            id=preceptor_id,
            firstname=firstname,
            lastname=lastname,
            schedule=schedule
        )
        toUpdate_preceptor.update()
        #HttpResponse solo para testear
        return HttpResponse('Preceptor actualizado')
    except:
        #HttpResponse solo para testear
        return HttpResponse('Error al actualizar el preceptor')


#Funcion de Borrar Preceptor
def deletePreceptor(request, preceptor_id):
    try:
        get_preceptor = Preceptor.objects.get(id=preceptor_id)          
        get_preceptor.delete()
        #HttpResponse solo para testear
        return HttpResponse("Preceptor eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el preceptor")

#Funcion de Crear Tutor
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


#Funcion de Actualizar Tutor
def updateTutor(request, tutor_id):
    firstname = request.POST['toUpdate_tutor_firstname']
    lastname = request.POST['toUpdate_tutor_lastname']
    phone = request.POST['toUpdate_tutor_phone']
    email = request.POST['toUpdate_tutor_email']
    try:
        get_device = Device.objects.get(id=request.POST['toUpdate_tutor_device'])
        toUpdate_tutor = Tutor(
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            email=email,
            device=get_device
        )
        toUpdate_tutor.update()
        #HttpResponse solo para testear
        return HttpResponse("Tutor actualizado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al actualizar el tutor")


#Funcion de Borrar Tutor
def deleteTutor(request, tutor_id):
    try:
        get_tutor = Tutor.objects.get(id=tutor_id)          
        get_tutor.delete()
        #HttpResponse solo para testear
        return HttpResponse("Tutor eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el Tutor")


#Funcion de Crear Estudiante
def createStudent(request):
    firstname = request.POST['student_firstname']
    lastname = request.POST['student_lastname']
    birthday = request.POST['student_birthday']
    dni = request.POST['student_dni']
    list_number = request.POST['student_list_number']
    student_tag = request.POST['student_student_tag']
    address = request.POST['student_address']
    city = request.POST['student_city']
    phone = request.POST['student_phone']
    status = request.POST['student_status']
    food_obvs = request.POST['student_food_obvs']
    try:
        get_curso = Curso.objects.get(id=request.POST['student_curso'])
        #Toma datos de una lista de un input (mucho a muchos), corregir en caso de no funcionar
        get_tutores = Tutor.objects.filter(id__in=request.POST['student_tutores'])
        new_student = Student(
            firstname=firstname,
            lastname=lastname,
            dni=dni,
            birthday=birthday,
            list_number=list_number,
            student_tag=student_tag,
            address=address,
            city=city,
            phone=phone,
            status=status,
            food_obvs=food_obvs,
            tutores=get_tutores,
            curso=get_curso
        )
        new_student.save()
        #HttpResponse solo para testear
        return HttpResponse("Alumno creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear el alumno")


#Funcion de Actualizar Estudiante
def updateStudent(request, student_id):
    firstname = request.POST['toUpdate_student_firstname']
    lastname = request.POST['toUpdate_student_lastname']
    birthday = request.POST['toUpdate_student_birthday']
    dni = request.POST['toUpdate_student_dni']
    list_number = request.POST['toUpdate_student_list_number']
    student_tag = request.POST['toUpdate_student_student_tag']
    address = request.POST['toUpdate_student_address']
    city = request.POST['toUpdate_student_city']
    phone = request.POST['toUpdate_student_phone']
    status = request.POST['toUpdate_student_status']
    food_obvs = request.POST['toUpdate_student_food_obvs']
    try:
        get_curso = Curso.objects.get(id=request.POST['toUpdate_student_curso'])
        #Toma datos de una lista de un input (mucho a muchos),TODO corregir en caso de no funcionar
        get_tutores = Tutor.objects.filter(id__in=request.POST['toUpdate_student_tutores'])
        toUpdate_student = Student(
            id=student_id,
            firstname=firstname,
            lastname=lastname,
            dni=dni,
            birthday=birthday,
            list_number=list_number,
            student_tag=student_tag,
            address=address,
            city=city,
            phone=phone,
            status=status,
            food_obvs=food_obvs,
            tutores=get_tutores,
            curso=get_curso
        )
        toUpdate_student.update()
        #HttpResponse solo para testear
        return HttpResponse("Alumno actualizado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al actualizar el alumno")


#Funcion de Borrar Estudiantes
def deleteStudent(request, student_id):
    try:
        get_student = Student.objects.get(id=student_id)          
        get_student.delete()
        #HttpResponse solo para testear
        return HttpResponse("Alumno eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el alumno")


#Funcion de Crear un Formulario N°2 
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


#Funcion de Actualizar el Formulario N°2
def updateF2(request, form2_id):
    schedule = request.POST['toUpdate_f2_schedule']
    try:
        get_student = Student.objects.get(id=request.POST['toUpdate_f2_student'])
        get_preceptor = Preceptor.objects.get(id=request.POST['toUpdate_f2_preceptor'])
        toUpdate_f2 = Form2(
            id=form2_id,
            student=get_student,
            preceptor=get_preceptor,
            schedule=schedule
        )
        toUpdate_f3.update()
        #HttpResponse solo para testear
        return HttpResponse('F2 actualizado')
    except:
        #HttpResponse solo para testear
        return HttpResponse('Error al actualizar el F2')


#Funcion de Borrar el Formulario N°2
def deleteF2(request, form2_id):
    try:
        get_f2 = Form2.objects.get(id=form2_id)          
        get_f2.delete()
        #HttpResponse solo para testear
        return HttpResponse("F2 eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el F2")


#Funcion de Crear un Formulario N°3
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


#Funcion de Actualizar el Formulario N°3
def updateF3(request, form3_id):
    schedule = request.POST['toUpdate_f3_schedule']
    reason = request.POST['toUpdate_f3_reason']
    try:
        get_student = Student.objects.get(id=request.POST['toUpdate_f3_student'])
        get_preceptor = Preceptor.objects.get(id=request.POST['toUpdate_f3_preceptor'])
        toUpdate_f3 = Form3(
            id=form3_id,
            student=get_student,
            preceptor=get_preceptor,
            reason=reason,
            schedule=schedule
        )
        toUpdate_f3.update()
        #HttpResponse solo para testear
        return HttpResponse('F3 actualizado')
    except:
        #HttpResponse solo para testear
        return HttpResponse('Error al actualizar el F3')


#Funcion de Borrar el Formulario N°3
def deleteF3(request, form3_id):
    try:
        get_f3 = Form3.objects.get(id=form3_id)          
        get_f3.delete()
        #HttpResponse solo para testear
        return HttpResponse("F3 eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el F3")


#Funcion de Crear Curso
def createCourse(request):
    year = request.POST['course_year']
    division = request.POST['course_division']
    try:
        #TODO: Corregir query, retorna un preceptor en vez de varios, usar filter() en vez de get()
        get_preceptores = Preceptor.objects.get(id=request.POST['course_preceptor'])
        new_course = Curso(year=year, division=division, preceptores=get_preceptores)
        new_course.save()
        #HttpResponse solo para testear
        return HttpResponse("Curso creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al creado el curso")


#Funcion de Actualizar Curso
def updateCourse(request, course_id):
    year = request.POST['toUpdate_course_year']
    division = request.POST['toUpdate_course_division']
    try:
        #TODO: Corregir query, retorna un preceptor en vez de varios, usar filter() en vez de get()
        get_preceptores = Preceptor.objects.get(id=request.POST['toUpdate_course_preceptor'])
        toUpdate_course = Curso(
            year=year,
            division=division,
            preceptores=get_preceptores
        )
        toUpdate_course.update()
        #HttpResponse solo para testear
        return HttpResponse("Curso actualizado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al actualizar el curso")


#Funcion de Borrar Curso
def deleteCourse(request, course_id):
    try:
        get_course = Curso.objects.get(id=course_id)          
        get_course.delete()
        #HttpResponse solo para testear
        return HttpResponse("Curso eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el curso")


#Funcion de Crear Ausencia
def createAbsence(request):
    justified = request.POST['absence_justified']
    percentage = request.POST['absence_percentage']
    try:
        student = Student.objects.get(id=request.POST['absence_student'])
        new_absence = Absence(
            justified=justified,
            percentage=percentage,
            student=student
        )
        #HttpResponse solo para testear
        return HttpResponse("Asistencia creada")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear la asistencia")


#Funcion de Actualizar Ausencia
def updateAbsence(request, absence_id):
    try:
        get_student = Student.objects.get(id=request.POST['toUpdate_absence_student'])
        toUpdate_absence = Absence(
            id=absence_id,
            justified=request.POST['toUpdate_absence_justified'],
            percentage=request.POST['toUpdate_absence_percentage'],
            student=student
        )
        toUpdate_device.update()
        #HttpResponse solo para testear
        return HttpResponse('Asistencia actualizada')
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al actualizar la asistencia")


#Funcion de Borrar Ausencia
def deleteAbsence(request, abscence_id):
    try:
        get_abscence = Abscence.objects.get(id=abscence_id)          
        get_abscence.delete()
        #HttpResponse solo para testear
        return HttpResponse("Asistencia eliminada")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar la asistencia")


#Funcion de Crear un Dispositivo
def createDevice(request):
    token = request.POST['device_token']
    try:
        new_device = Device(token=token)
        new_device.save()
        #HttpResponse solo para testear
        return HttpResponse('Dispositivo creado')
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear el dispositivo")



#Funcion de Actualizar un Dispositivo
def updateDevice(request, device_id):
    try:
        toUpdate_device = Device(id=device_id, token=request.POST['toUpdate_device_token'])
        toUpdate_device.update()
        #HttpResponse solo para testear
        return HttpResponse('Dispositivo actualizado')
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al actualizar el dispositivo")


#Funcion de Borrar un Dispositivo
def deleteDevice(request, device_id):
    try:
        get_device = Device.objects.get(id=device_id)          
        get_device.delete()
        #HttpResponse solo para testear
        return HttpResponse("Dispositivo eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el dispositivo")



#Funcion para Crear un Curso Auxiliar
def createAuxiliarCourse(request):
    try:
        new_auxCourse = Curso_aux(
            preceptor=request.POST['auxCourse_preceptor'],
            curso=request.POST['auxCourse_curso']
        )
        new_auxCourse.save()
        #HttpResponse solo para testear
        return HttpResponse("Curso auxiliar creado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al crear el curso auxiliar")



#Funcion de Actualizar Curso Auxiliar
def updateAuxiliarCourse(request, auxCourse_id):
    try:
        get_preceptor = Preceptor.objects.get(id=request.POST['toUpdate_auxCourse_preceptor'])
        get_course = Curso.objects.get(id=request.POST['toUpdate_auxCourse_course'])          
        update_auxCourse = Curso_aux(
            id=auxCourse_id,
            preceptor=get_preceptor,
            curso=get_course
        )
        update_auxCourse.update()
        #HttpResponse solo para testear
        return HttpResponse("Curso auxiliar actualizado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al actualizar el curso auxiliar")



#Funcion de Elimar Clase Auxiliar
def deleteAuxiliarCourse(request, auxCourse_id):
    try:
        get_auxCourse = Curso_aux.objects.get(id=auxCourse_id)          
        get_auxCourse.delete()
        #HttpResponse solo para testear
        return HttpResponse("Curso auxiliar eliminado")
    except:
        #HttpResponse solo para testear
        return HttpResponse("Error al eliminar el curso auxiliar")