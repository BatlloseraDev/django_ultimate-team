from django.shortcuts import render
import json
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Rol
from datetime import datetime
# Create your views here.

def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            nick = data.get('nick')
            correo = data.get('correo')
            password = data.get('password')
            rol = data.get('rol')
            fecha_nacimiento = data.get('fecha_nacimiento')
            fecha_registro = data.get('fecha_registro')
            equipo = data.get('equipo')

            if not (nombre and correo):
                return JsonResponse({'ok': False, 'error': 'Faltan campos obligatorios'}, status=400)

            # Convertir la fecha
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()

            # Crear el usuario
            usuario = Usuario.objects.create(
                nombre=nombre,
                nick=nick,
                correo=correo,
                password=password,
                rol=rol,
                fecha_nacimiento=fecha_nacimiento,
                fecha_registro=fecha_registro,
                equipo=equipo,
            )

            return JsonResponse({
                'ok': True,
                'data': {
                    'nombre': nombre,
                    'nick': nick,
                    'fecha_registro': fecha_registro
                }

            }, status=200  )


        except json.JSONDecodeError:

            return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

        except ValueError as e:

            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

    else:

        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


# Mostrar todos los usuarios
def get_users(request):
    if request.method == 'GET':
      try:
        usuarios = Usuario.objects.all().values()
        return JsonResponse({'ok': True, 'usuarios': list(usuarios)}, status=200)
      except:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


#Mostrar a un usuario por id
def get_user(request, id):
    if request.method == 'GET':
        data = Usuario.objects.filter(id=id).values()
        if data:
            return JsonResponse({'ok': True, 'usuario': list(data)[0]}, status=200)
        else:
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=404)
    return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


#Borrar usuario
def delete_user(request, id):
    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return JsonResponse({'ok': True}, status=200)
        except Usuario.DoesNotExist:
             return JsonResponse({'ok': False}, status=404)

# Modificar usuario
def update_user(request, id):
    if request.method == 'PUT':
        try:
            usuario = Usuario.objects.get(id=id)
            data = json.loads(request.body)

            # Actualizar solo los campos que vienen en el body
            if 'nombre' in data:
                usuario.nombre = data['nombre']
            if 'nick' in data:
                usuario.nick = data['nick']
            if 'correo' in data:
                usuario.correo = data['correo']
            if 'password' in data:
                usuario.password = data['password']
            if 'rol' in data:
                usuario.rol = data['rol']
            if 'fecha_nacimiento' in data:
                usuario.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
            if 'fecha_registro' in data:
                usuario.fecha_registro = datetime.strptime(data['fecha_registro'], '%Y-%m-%d %H:%M:%S')
            if 'equipo' in data:
                usuario.equipo = data['equipo']

            usuario.save()

            return JsonResponse({'ok': True, 'mensaje': 'Usuario actualizado correctamente'}, status=200)

        except Usuario.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=404)
        except ValueError as e:
            return JsonResponse({'ok': False, 'error': f'Error en formato de fecha: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

    return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

@csrf_exempt
def asignar_rol(request, id):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id=id)
            data = json.loads(request.body)
            rol_nombre = data.get('rol')

            if not rol_nombre:
                return JsonResponse({'ok': False, 'error': 'No se proporcionó el nombre del rol'}, status=400)

            rol_asignado = Rol.objects.filter(nombre=rol_nombre).first()

            if not rol_asignado:
                return JsonResponse({'ok': False, 'error': 'Rol no encontrado'}, status=404)

            if usuario.rol.filter(nombre=rol_nombre).exists():
                return JsonResponse({'ok':False, 'error': 'El usuario ya tiene ese rol asignado'}, status=400)

            usuario.rol.add(rol_asignado)
            usuario.save()

            return JsonResponse({'ok': True, 'mensaje': f'Rol "{rol_nombre}" asignado correctamente'}, status=200)

        except Usuario.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

def eliminar_rol(request, id):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id=id)

            data = json.loads(request.body)
            rol_nombre = data.get('rol')


            if not rol_nombre:
                return JsonResponse({'ok': False, 'error': 'No se proporcionó el nombre del rol'}, status=400)

            rol_desagsinar =  Rol.objects.filter(nombre=rol_nombre).first()

            if not usuario.rol.filter(nombre=rol_nombre).exists():
                return JsonResponse({'ok': False, 'error': 'El usuario no tenia ese rol'}, status=404)

            if not rol_desagsinar:
                return JsonResponse({'ok': False, 'error': 'Rol no encontrado'}, status=404)

            usuario.rol.remove(rol_desagsinar)
            return JsonResponse({'ok': True, 'mensaje': 'Rol eliminado correctamente'}, status=200)
        except Usuario.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)