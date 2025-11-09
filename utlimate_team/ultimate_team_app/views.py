from django.shortcuts import render
import random
from django.db import IntegrityError
import json
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Rol, Jugador, Equipo, Posicion, Nacionalidad
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
            rol_nombre = data.get('rol')
            fecha_nacimiento = data.get('fecha_nacimiento')
            fecha_registro = data.get('fecha_registro')
            equipo = data.get('equipo')

            if not (password and correo and nombre):
                return JsonResponse({'ok': False, 'error': 'Faltan campos obligatorios'}, status=400)

            correos = Usuario.objects.values_list('correo', flat=True)

            if correo in correos:
                return JsonResponse({'ok': False, 'error': 'Correo ya existente'}, status=400)

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

            if not rol_nombre:
                return JsonResponse({'ok': False, 'error': 'No se proporcionó el nombre del rol'}, status=400)

            rol_asignado = Rol.objects.filter(nombre=rol_nombre).first()

            if not rol_asignado:
                return JsonResponse({'ok': False, 'error': 'Rol no encontrado'}, status=404)

            if usuario.rol.filter(nombre=rol_nombre).exists():
                return JsonResponse({'ok': False, 'error': 'El usuario ya tiene ese rol asignado'}, status=400)

            usuario.rol.add(rol_asignado)
            usuario.save()

            return JsonResponse({
                'ok': True,
                'data': {
                    'nombre': nombre,
                    'nick': nick,
                    'fecha_registro': fecha_registro
                }

            }, status=201  )


        except json.JSONDecodeError:

            return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

        except ValueError as e:

            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

    else:

        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


# Mostrar todos los usuarios
def get_users(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all().values()
        return JsonResponse({'ok': True, 'usuarios': list(usuarios)}, status=200)
    else:
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

            campos = ['nombre', 'nick', 'correo', 'password', 'rol', 'fecha_nacimiento', 'fecha_registro',
                              'equipo']

            for campo in data:
                if campo not in campos:
                    return JsonResponse({'ok': False, 'error': 'No existe ese campo'}, status=400)

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
    """Asigna jugadores aleatorios a un equipo dado."""
    jugadores_disponibles = Jugador.objects.all()

    if jugadores_disponibles.count() < 23:
        raise ValueError('No hay suficientes jugadores disponibles para crear un equipo (mínimo 23).')

    porteros = list(jugadores_disponibles.filter(posicion_id__tipo='POR'))
    defensas = list(jugadores_disponibles.filter(posicion_id__tipo='DEF'))
    centrocampistas = list(jugadores_disponibles.filter(posicion_id__tipo='CEN'))
    delanteros = list(jugadores_disponibles.filter(posicion_id__tipo='DEL'))

    if len(porteros) < 2 or len(defensas) < 8 or len(centrocampistas) < 6 or len(delanteros) < 5:
        raise ValueError('No hay suficientes jugadores en alguna posición para formar un equipo completo.')

    seleccionados=[]

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

@csrf_exempt
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

@csrf_exempt
def add_jugador(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            nacionalidad = Nacionalidad.objects.get(id=data.get('nacionalidad'))
            equipo = data.get('equipo')
            posicion_id = Posicion.objects.get(tipo=data.get('posicion_id'))
            pac = data.get('pac')
            sho = data.get('sho')
            pas = data.get('pas')
            dri = data.get('dri')
            defe = data.get('defe')
            phy = data.get('phy')

            jugador = Jugador.objects.create(
                nombre=nombre,
                nacionalidad=nacionalidad,
                equipo=equipo,
                posicion_id=posicion_id,
                pac=pac,
                sho=sho,
                pas=pas,
                dri=dri,
                defe=defe,
                phy=phy
            )

            return JsonResponse({'ok': True, 'jugador': jugador.nombre, 'id': jugador.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'ok': False, 'error': f'Error de base de datos: {str(e)}'}, status=400)
        except ValueError as e:
            return JsonResponse({'ok': False, 'error': f'Error de tipo de dato: {str(e)} '}, status=500)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error desconocido: {str(e)}'}, status=500)
    else:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


def get_jugador(request, id):
    if request.method == 'GET':
        try:
            jugador = Jugador.objects.get(id=id)
            return JsonResponse({'ok': True, 'jugador': jugador.nombre}, status=200)
        except Jugador.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Jugador no encontrado'}, status=404)
        except ValueError as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


def get_jugadores(request):
   if request.method == 'GET':
       try:
           jugadores = Jugador.objects.all()
           jugadores_data = []
           for jugador in jugadores:
               jugadores_data.append({
                   'id': jugador.id,
                   'nombre': jugador.nombre,
                   'equipo': jugador.equipo,
                   'pac': jugador.pac,
                   'sho': jugador.sho,
                   'pas': jugador.pas,
                   'dri': jugador.dri,
                   'defe': jugador.defe,
                   'phy': jugador.phy,
               })
           return JsonResponse({'ok': True, 'jugadores': jugadores_data}, status=200)
       except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error desconocido:{str(e)}'}, status=500)
   else:
       return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)
@csrf_exempt
def delete_jugador(request, id):
    if request.method == 'DELETE':
        try:
            jugador = Jugador.objects.get(id=id)

            equipos_con_jugador = Equipo.objects.filter(jugadores=jugador)

            if equipos_con_jugador.exists():
                nombres_equipos = list(equipos_con_jugador.values_list('nombre', flat=True))
                return JsonResponse({
                    'ok': False,
                    'error': f'No se puede eliminar el jugador. Está asignado a los equipos: {", ".join(nombres_equipos)}. Retire al jugador de todos los equipos antes de eliminarlo.'
                }, status=400)

            jugador.desactivado = True
            jugador.save()

            return JsonResponse({
                'ok': True,
                'mensaje': 'Jugador eliminado correctamente (eliminación pasiva)'
            }, status=200)

        except Jugador.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Jugador no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error desconocido:{str(e)}'}, status=500)
    else:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


@csrf_exempt
def update_jugador(request):
    if request.method == 'PUT':
        try:
            id = request.GET.get('id')
            jugador = Jugador.objects.get(id=id)
            data = json.loads(request.body)

            jugador.nombre = data.get('nombre')
            jugador.nacionalidad = Nacionalidad.objects.get(id=data.get('nacionalidad')) #data.get('nacionalidad')
            jugador.equipo = data.get('equipo')
            jugador.posicion_id = Posicion.objects.get(tipo=data.get('posicion_id'))
            jugador.pac = data.get('pac')
            jugador.sho = data.get('sho')
            jugador.pas = data.get('pas')
            jugador.dri = data.get('dri')
            jugador.defe = data.get('defe')
            jugador.phy = data.get('phy')

            jugador.save()
            return JsonResponse({'ok': True, 'jugador': jugador.nombre}, status=200)
        except Jugador.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Jugador no encontrado'}, status=404)
        except IntegrityError as e:
            return JsonResponse({'ok': False, 'error': f'Error de base de datos: {str(e)}'}, status=400)
        except ValueError as e:
            return JsonResponse({'ok': False, 'error': f'Error de tipo de dato: {str(e)} '}, status=500)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error desconocido:{str(e)}'}, status=500)
    else:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

@csrf_exempt
def add_jugador_equipo(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            jugador = Jugador.objects.get(id=id)

            if not Equipo.objects.filter(id_usuario=data.get('id_usuario')).exists():
                return JsonResponse({'ok': False, 'error': 'No se ha encontrado nigun equipo con ese id de usuario'}, status=404)
            equipo = Equipo.objects.get(id_usuario=data.get('id_usuario'))

            if equipo.jugadores.filter(id=jugador.id).exists():
                return JsonResponse({'ok': False, 'error': 'El jugador ya está en el equipo'}, status=400)

            numero_jugadores_actual = equipo.jugadores.count()
            max_jugadores_equipo = 25 #debería de ser una variable global para poder cambiar este parametro

            if numero_jugadores_actual >= max_jugadores_equipo:
                return JsonResponse({
                    'ok': False,
                    'error': f'El equipo ya tiene el máximo de {max_jugadores_equipo} jugadores'},
                    status=400)

            equipo.jugadores.add(jugador)
            return JsonResponse({
                'ok': True,
                'mensaje': 'Jugador agregado al equipo correctamente',
                'jugadores_en_equipo': equipo.jugadores.count()},
                status=200)

        except Jugador.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Jugador no encontrado'}, status=404)
        except Equipo.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Equipo no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error desconocido:{str(e)}'}, status=500)
    else:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)

@csrf_exempt
def delete_jugador_equipo(request, id):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            jugador = Jugador.objects.get(id=id)
            equipo = Equipo.objects.get(id_usuario=data.get('id_usuario'))
            if not equipo.jugadores.filter(id=jugador.id).exists():
                return JsonResponse({'ok': False, 'error': 'El jugador no existe en el equipo'}, status=400)
            equipo.jugadores.remove(jugador)
            return JsonResponse({'ok': True, 'mensaje': 'Jugador eliminado del equipo correctamente'}, status=200)
        except Jugador.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Jugador no encontrado'}, status=404)
        except Equipo.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Equipo no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': f'Error desconocido:{str(e)}'}, status=500)
    else:
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)