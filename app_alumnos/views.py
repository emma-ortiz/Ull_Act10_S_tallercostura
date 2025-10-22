# views.py

from django.http import HttpResponseRedirect
from django.shortcuts import render 
from django.urls import reverse 

from .models import Alumno
from .forms import AlumnoForm

def index(request):
    return render(request, 'alumnos/index.html', {
        'alumnos': Alumno.objects.all()
    })

def view_alumno(request, id):
    # Error tipográfico: obecjects -> objects.get
    # Debes usar .get() para obtener un solo alumno
    try:
        alumno = Alumno.objects.get(pk=id)
        return render(request, 'alumnos/view_alumno.html', {
            'alumno': alumno
        })
    except Alumno.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    

def add(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            
            # Puedes usar .save() directamente para ModelForms
            # form.save()
            
            # O guardar manualmente (corregido el error 'claned_data'):
            nombre_limpio = form.cleaned_data['nombre']
            apellido_paterno = form.cleaned_data['apellido_paterno']
            apellido_materno = form.cleaned_data['apellido_materno'] # Corregido: 'claned_data' a 'cleaned_data'
            edad = form.cleaned_data['edad']
            genero = form.cleaned_data['genero']
            correo = form.cleaned_data['correo']


            new_alumno = Alumno(
                nombre=nombre_limpio,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                edad=edad,
                genero=genero,
                correo=correo
            )

            new_alumno.save()
            return render(request , 'alumnos/add.html',{
                'form': AlumnoForm(), # Muestra un formulario vacío después del éxito
                'success': True
            })
    else:
        form = AlumnoForm() # Inicializa el formulario para GET
        
    return render(request , 'alumnos/add.html',{
        'form': form # Usa la variable 'form'
    })

# views.py

# Asegúrate de que tu función 'edit' se vea así:

def edit(request, id):
    try:
        # 1. Recuperamos el alumno primero
        alumno = Alumno.objects.get(pk=id)
    except Alumno.DoesNotExist:
        # Manejo de error si no existe el ID
        return HttpResponseRedirect(reverse('index')) 

    if request.method == "POST":
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            
            # CORRECCIÓN: Renderizar el template con 'success' en True
            return render(request, 'alumnos/edit.html', {
                'form': form,
                'alumno': alumno,   # Necesario para el contexto
                'success': True     # Activa el mensaje de éxito en edit.html
            })
        
        # Si el POST falla (no es válido), el código sigue y renderiza el formulario con errores

    else: # Solicitud GET
        # 2. Creamos el formulario precargado para mostrarlo inicialmente
        form = AlumnoForm(instance=alumno)
        
    # Esta línea se ejecuta en GET (para mostrar el form) o en POST fallido.
    return render(request, 'alumnos/edit.html', {
        'form': form, 
        'alumno': alumno 
    })

def delete(request, id): # Cambié 'rquest' a 'request' y corregí la indentación
    if request.method == "POST":
        alumno = Alumno.objects.get(pk=id)
        alumno.delete()
    return HttpResponseRedirect(reverse('index'))