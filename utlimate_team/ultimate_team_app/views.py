import random
from django.shortcuts import render
import json
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt

from .models import Usuario, Equipo, Jugador
from datetime import datetime
# Create your views here.

@csrf_exempt
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
                fecha_nacimiento=fecha_nacimiento,
                fecha_registro=fecha_registro,
                equipo=equipo,
            )

            if rol:
                usuario.rol.set(rol)

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
@csrf_exempt
def delete_user(request, id):
    if request.method == 'DELETE':
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return JsonResponse({'ok': True, 'mensaje':'Usuario eliminado correctamente'}, status=200)
        except Usuario.DoesNotExist:
             return JsonResponse({'ok': False, 'error':'El usuario no existe'}, status=404)

# Modificar usuario
@csrf_exempt
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

def asignar_jugadores_equipo(equipo):
    """Asigna jugadores aleatorios sin equipo a un equipo dado."""
    jugadores_disponibles = Jugador.objects.filter(equipo=None)

    if jugadores_disponibles.count() < 23:
        raise ValueError('No hay suficientes jugadores disponibles para crear un equipo (mínimo 23).')

    porteros = list(jugadores_disponibles.filter(posicion_id__tipo='POR'))
    defensas = list(jugadores_disponibles.filter(posicion_id__tipo='DEF'))
    centrocampistas = list(jugadores_disponibles.filter(posicion_id__tipo='CEN'))
    delanteros = list(jugadores_disponibles.filter(posicion_id__tipo='DEL'))

    if len(porteros) < 2 or len(defensas) < 8 or len(centrocampistas) < 6 or len(delanteros) < 5:
        raise ValueError('No hay suficientes jugadores en alguna posición para formar un equipo completo.')

    while not 23 <= len(seleccionados) <= 25:
        seleccionados = (
            random.sample(porteros, random.randint(2, min(3, len(porteros)))) +
            random.sample(defensas, random.randint(8, min(10, len(defensas)))) +
            random.sample(centrocampistas, random.randint(6, min(9, len(centrocampistas)))) +
            random.sample(delanteros, random.randint(5, min(6, len(delanteros))))
        )

    # Limitar total entre 23 y 25 jugadores


    equipo.jugadores.add(*seleccionados)
    return seleccionados


@csrf_exempt
def asignar_equipo(request, id):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido.'}, status=405)

    try:
        if not Usuario.objects.filter(id=id).exists():
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado.'}, status=404)
        usuario = Usuario.objects.get(id=id)

        # Comprobamos si ya tiene un equipo
        if Equipo.objects.filter(id_usuario=usuario).exists():
            return JsonResponse({'ok': False, 'error': 'El usuario ya tiene un equipo asignado.'}, status=400)

        data = json.loads(request.body)
        nombre = data.get('nombre')
        descripcion = data.get('descripcion', '')

        if not nombre:
            return JsonResponse({'ok': False, 'error': 'El nombre del equipo es obligatorio.'}, status=400)


        equipo = Equipo.objects.create(
            nombre=nombre,
            id_usuario=usuario,
            descripcion=descripcion
        )


        try:
            jugadores = asignar_jugadores_equipo(equipo)
        except ValueError as e:
            equipo.delete()
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

        jugadores_info = [
            {'nombre': j.nombre, 'posicion': j.posicion_id.tipo}
            for j in jugadores
        ]

        return JsonResponse({
            'ok': True,
            'mensaje': 'Equipo creado correctamente y asignado al usuario.',
            'equipo': {
                'id': equipo.id,
                'nombre': equipo.nombre,
                'descripcion': equipo.descripcion,
                'usuario': usuario.nombre
            },
            'jugadores': jugadores_info
        }, status=201)

    except Usuario.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Usuario no encontrado.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'JSON inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)

def consultar_equipo(request, id):
    if request.method == 'GET':
        if not Usuario.objects.filter(id=id).exists():
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado.'}, status=404)
        try:
            equipo = Equipo.objects.get(id_usuario=id)
            jugadores = equipo.jugadores.all()


            jugadores_info = []
            for j in jugadores:
                jugadores_info.append({
                    'id': j.id,
                    'nombre': j.nombre,
                    'posicion': j.posicion_id.tipo
                })

            return JsonResponse({
                'ok': True,
                'equipo': {
                    'id': equipo.id,
                    'nombre': equipo.nombre,
                    'descripcion': equipo.descripcion,
                    'usuario': equipo.id_usuario.nombre
                },
                'jugadores': jugadores_info
            }, status=200)

        except Equipo.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Equipo no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=500)

    return JsonResponse({'ok': False, 'error': 'Método no permitido.'}, status=405)
