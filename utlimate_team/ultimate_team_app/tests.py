from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Usuario, Rol, Posicion, Jugador, Nacionalidad, Equipo
#from ..datos.cargar_nacionalidades import nombre


# Create your tests here.
class AdminApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_admin = Rol.objects.create(
            nombre='administrador',
        )

        cls.rol_usuario = Rol.objects.create(
            nombre='usuario',
        )
        cls.nacionalidad_argentina = Nacionalidad.objects.create(
            nombre='Argentina'
        )

        cls.posicion_delantero, created = Posicion.objects.get_or_create(
            tipo='DEL',
            siglas='DEL',
            defaults={'significado': 'Delantero'}
        )

        cls.posicion_portero, created = Posicion.objects.get_or_create(
            tipo='POR',
            siglas='POR',
            defaults={'significado': 'Portero'}
        )

        cls.posicion_defensa, created = Posicion.objects.get_or_create(
            tipo='DEF',
            siglas='DEF',
            defaults={'significado': 'Defensa'}
        )
        cls.usuario = Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='marta@gmail.com',
            password='12345',
            fecha_nacimiento='2006-09-21'
            )
        rol = Rol.objects.get(nombre="administrador")
        cls.usuario.rol.set([rol])

        cls.nacionalidad_espana = Nacionalidad.objects.create(
            nombre='España'
        )

        cls.jugador_casillas = Jugador.objects.create(
            nombre="Iker Casillas",
            nacionalidad=cls.nacionalidad_espana,
            equipo="Real Madrid",
            posicion_id=cls.posicion_portero,
            pac=84,
            sho=70,
            pas=77,
            dri=69,
            defe=85,
            phy=84
        )

    def test_crear_usuario_valido(self):
        """Comprobamos que se puede crear un usuario correctamente"""
        url = reverse('add_user')
        data = {
            "nombre": "Marta Frontón",
            "nick": "mfronton",
            "correo": "marta.fronton@example.com",
            "password": "12345",
            "rol": "administrador",
            "fecha_nacimiento": "2002-06-15",
            "fecha_registro": "2025-11-08",
            "equipo": 3
        }

        response = self.client.post(url, data=data, content_type="application/json")
        self.assertTrue(Usuario.objects.filter(nick='mfronton').exists())
        self.assertEqual(response.status_code, 201)

    def test_crear_usuario_error(self):
        """Al no dar un nombre no se permite crear la creación de un usuario"""
        url = reverse('add_user')
        data = {
            "nombre": "",  # nombre vacío
            "nick": "mfronton",
            "correo": "martafronton@example.com",
            "password": "12345",
            "rol": "administrador",
            "fecha_nacimiento": "2002-06-15"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_mostrar_usuarios_valido(self):
        """Comprobamos que se muestran todos los usuarios correctamente"""
        url=reverse('get_users')
        usuario=Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='martafronton@gmail.com',
            password="12345",
            fecha_nacimiento='2006-09-21'
        )
        usuario.rol.set([1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Usuario.objects.count(), 2)

    def test_mostrar_usuarios_error(self):
        """Utilizar un método que no sea GET"""
        url = reverse('get_users')
        response = self.client.post(url)  # POST en vez de GET
        self.assertEqual(response.status_code, 405)

    def test_mostrar_usuario(self):
        """Comprobamos que podemos obtener un usuario por id"""
        url = reverse('get_user', args=[self.usuario.id])
        response=self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('marta', response.content.decode())

    def test_mostrar_usuario_invalido(self):
        """Intentamos obtener un usuario que no existe"""
        url = reverse('get_user', args=[999])  # ID que no existe
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_borrar_usuario(self):
        """Comprobamos que podemos borrar a un usuario correctamente"""
        url = reverse('delete_user', args=[self.usuario.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_borrar_usuario_invalido(self):
        """Intentamos borrar a un usuario que no existe"""
        url = reverse('delete_user', args=[999])  # ID que no existe
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_actualizar_usuario_valido(self):
        """Comprobamos que podemos actualizar el nombre de un usuario correctamente"""
        url=reverse('update_user', args=[self.usuario.id])
        data = {
            "nombre":"Laura"
        }
        response = self.client.put(url, data=data, content_type="application/json")
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nombre, "Laura")
        self.assertEqual(response.status_code, 200)

    def test_actualizar_usuario_error(self):
        """Intentamos actualizar un campo que no existe"""
        url=reverse('update_user', args=[self.usuario.id])
        data={
            "apellido":"Frontón"
        }
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_add_jugador_valido(self):
        """Compruebo que podamos añadir un jugador correctamente a la pool"""
        url = reverse('add_jugador')
        data={
            "nombre":"Messi",
            "nacionalidad":1,
            "equipo":"nosé",
            "posicion_id":'DEL',
            "pac":90,
            "sho":90,
            "pas":90,
            "dri":90,
            "defe":90,
            "phy":90
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_add_jugador_invalido(self):
        """Test con datos inválidos para verificar manejo de errores"""
        url = reverse('add_jugador')
        data = {
            "nombre": "",
            "nacionalidad": 9999,
            "posicion_id": "POS_INVALIDA",  #
            "pac": 150,
            "sho": 90,
            "pas": 90,
            "dri": 90,
            "defe": 90,
            "phy": 90
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_get_jugador_valido(self):
        """Comprobamos que podemos obtener un jugador correctamente"""
        url = reverse('get_jugador', args=[self.jugador_casillas.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertTrue(response_data['ok'])
        self.assertEqual(response_data['jugador'], "Iker Casillas")

    def test_get_jugador_invalido(self):
        """Intentamos obtener un jugador que no existe"""
        url = reverse('get_jugador', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        response_data = response.json()
        self.assertFalse(response_data['ok'])
        self.assertIn('error', response_data)

    def test_get_jugadores_exito(self):
        """Comprobamos que podemos obtener todos los jugadores correctamente"""
        url = reverse('get_jugadores')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertTrue(response_data['ok'])
        self.assertGreater(len(response_data['jugadores']), 0)

    def test_get_jugadores_invalido(self):
        """Intentamos obtener jugadores metodo incorrecto"""
        url = reverse('get_jugadores')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 405)

    def test_delete_jugador(self):

        """Comprobamos que podemos eliminar un jugador correctamente"""
        url = reverse('delete_jugador', args=[self.jugador_casillas.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

        # Si hace eliminación pasiva, el jugador sigue existiendo pero desactivado, por si acaso meto el else
        if hasattr(self.jugador_casillas, 'desactivado'):
            self.jugador_casillas.refresh_from_db()
            self.assertTrue(self.jugador_casillas.desactivado)
        else:
            self.assertFalse(Jugador.objects.filter(id=self.jugador_casillas.id).exists())

    def test_delete_jugador_invalido(self):
        """Intentamos eliminar un jugador que no existe"""
        url = reverse('delete_jugador', args=[999])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

    def test_update_jugador_valido(self):
        """Comprobamos que podemos actualizar un jugador correctamente"""

        self.assertTrue(Jugador.objects.filter(id=self.jugador_casillas.id).exists())
        url = f"{reverse('update_jugador')}?id={self.jugador_casillas.id}"

        data = {
            "nombre": "Casillas Actualizado",
            "nacionalidad": self.jugador_casillas.nacionalidad.id,  # Valor actual
            "equipo": "Real Madrid Actualizado",
            "posicion_id": self.jugador_casillas.posicion_id.tipo,  # Valor actual
            "pac": self.jugador_casillas.pac,  # Valor actual
            "sho": self.jugador_casillas.sho,  # Valor actual
            "pas": self.jugador_casillas.pas,  # Valor actual
            "dri": self.jugador_casillas.dri,  # Valor actual
            "defe": self.jugador_casillas.defe,  # Valor actual
            "phy": self.jugador_casillas.phy  # Valor actual
        }

        response = self.client.put(
            url,
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)


    def test_update_jugador_invalido(self):
        """Intentamos actualizar un jugador que no existe"""
        url = reverse('update_jugador')
        data = {
            "id": 999,
            "nombre": "Iker Casillas",
            "nacionalidad": 1,
            "equipo": "Valladolid",
            "posicion_id": 'POR',
            "pac": 84,
            "sho": 70,
            "pas": 77,
            "dri": 69,
            "defe": 85,
            "phy": 84
        }
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)




class RolApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_admin = Rol.objects.create(
            nombre='administrador',
        )

        cls.rol_usuario = Rol.objects.create(
            nombre='usuario',
        )

        cls.usuario = Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='marta@gmail.com',
            password='12345',
            fecha_nacimiento='2006-09-21'
        )
        rol = Rol.objects.get(nombre="administrador")
        cls.usuario.rol.set([rol])

    def test_asignar_rol_valido(self):
        """Comprobamos que podemos asignar roles a los usuarios correctamente"""
        url = reverse('asignar_rol', args=[self.usuario.id])
        data={
            'rol':"usuario"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_asignar_rol_error(self):
        """Intentamos asignar un rol que no existe a un usuario"""
        url = reverse('asignar_rol', args=[self.usuario.id])
        data={
                'rol':"gestor"
            }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_eliminar_rol_valido(self):
        """Comprueba que se puede eliminar un rol de un usuario correctamente"""

        self.usuario.rol.add(self.rol_usuario)

        url = reverse('eliminar_rol', args=[self.usuario.id])
        data = {
            'rol': "usuario"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)


        self.usuario.refresh_from_db()
        self.assertFalse(self.usuario.rol.filter(nombre="usuario").exists())
        self.assertTrue(self.usuario.rol.filter(nombre="administrador").exists())

    def test_eliminar_rol_no_existe_usuario(self):
        """Intenta eliminar un rol de un usuario que no existe"""
        url = reverse('eliminar_rol', args=[999])  # ID que no existe
        data = {
            'rol': "usuario"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_eliminar_rol_usuario_no_tiene_rol(self):
        """Intenta eliminar un rol que el usuario no posee"""
        url = reverse('eliminar_rol', args=[self.usuario.id])
        data = {
            'rol': "gestor"  # Rol que no tiene asignado
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_eliminar_rol_sin_rol_proporcionado(self):
        """Intenta eliminar un rol sin proporcionar el nombre del rol"""
        url = reverse('eliminar_rol', args=[self.usuario.id])
        data = {}  # Sin el campo 'rol'
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_eliminar_rol_metodo_incorrecto(self):
        """Intenta eliminar un rol usando un método HTTP incorrecto"""
        url = reverse('eliminar_rol', args=[self.usuario.id])
        data = {
            'rol': "administrador"
        }
        # Usamos GET en lugar de POST
        response = self.client.get(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_eliminar_rol_todos_los_roles(self):
        """Comprueba que puede eliminar todos los roles de un usuario"""
        # Asignamos ambos roles
        self.usuario.rol.add(self.rol_usuario)

        # Primero eliminamos el rol de usuario
        url1 = reverse('eliminar_rol', args=[self.usuario.id])
        data1 = {'rol': "usuario"}
        response1 = self.client.post(url1, data=data1, content_type="application/json")
        self.assertEqual(response1.status_code, 200)

        # Ahora eliminamos el rol de administrador
        url2 = reverse('eliminar_rol', args=[self.usuario.id])
        data2 = {'rol': "administrador"}
        response2 = self.client.post(url2, data=data2, content_type="application/json")
        self.assertEqual(response2.status_code, 200)

        # Verificamos que el usuario ya no tiene ningún rol
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.rol.count(), 0)


class UsuarioTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rol_admin = Rol.objects.create(
            nombre='administrador',
        )

        cls.rol_usuario = Rol.objects.create(
            nombre='usuario',
        )

        cls.usuario = Usuario.objects.create(
            nombre='marta',
            nick='mar',
            correo='marta@gmail.com',
            password='12345',
            fecha_nacimiento='2006-09-21'
        )
        rol = Rol.objects.get(nombre="administrador")
        cls.usuario.rol.set([rol])

        cls.pos_por, _ = Posicion.objects.get_or_create(tipo='POR', siglas='POR')
        cls.pos_def, _ = Posicion.objects.get_or_create(tipo='DEF', siglas='DEF')
        cls.pos_cen, _ = Posicion.objects.get_or_create(tipo='CEN', siglas='CEN')
        cls.pos_del, _ = Posicion.objects.get_or_create(tipo='DEL', siglas='DEL')


        cls.nacionalidad = Nacionalidad.objects.create(nombre='España')

        cls.jugador_casillas = Jugador.objects.create(
            nombre="Iker Casillas",
            nacionalidad=cls.nacionalidad,
            equipo="Real Madrid",
            posicion_id=cls.pos_por,
            pac=84,
            sho=70,
            pas=77,
            dri=69,
            defe=85,
            phy=84
        )



        for i in range(3):
            Jugador.objects.create(nombre=f'Portero {i}', posicion_id=cls.pos_por, nacionalidad=cls.nacionalidad)
        for i in range(10):
            Jugador.objects.create(nombre=f'Defensa {i}', posicion_id=cls.pos_def, nacionalidad=cls.nacionalidad)
        for i in range(9):
            Jugador.objects.create(nombre=f'Centrocampista {i}', posicion_id=cls.pos_cen, nacionalidad=cls.nacionalidad)
        for i in range(6):
            Jugador.objects.create(nombre=f'Delantero {i}', posicion_id=cls.pos_del, nacionalidad=cls.nacionalidad)

    def test_asignar_equipo_valido(self):
        """Comprobamos que podemos asignar un equipo a un usuario correctamente"""
        url = reverse('asignar_equipo', args=[self.usuario.id])
        data={
          "nombre": "Argamasilla",
          "descripcion": "Equipo con espíritu competitivo"
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_asignar_equipo_error(self):
        """Intentamos asignar un equipo a un usuario que ya tiene un equipo"""
        Equipo.objects.create(
            nombre="Equipo previo",
            id_usuario=self.usuario,
            descripcion="Equipo ya existente"
        )

        url = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_consultar_equipo_valido(self):
        """Comprobamos que podemos consultar el equipo de un usuario correctamente"""
        # Primero asignamos un equipo
        url_asignar = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        self.client.post(url_asignar, data=data, content_type="application/json")

        url_consultar = reverse('consultar_equipo', args=[self.usuario.id])
        response = self.client.get(url_consultar, data={}, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_add_jugador_equipo_valido(self):
        """Comprobamos que podemos añadir un jugador a un equipo correctamente"""
        #Primeor asigno un equipo:
        url_asignar = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        self.client.post(url_asignar, data=data, content_type="application/json")

        #Compruebo que el equipo tenga menos de 25 jugadores si tiene 25 elimino el ultimo para poder hacer las pruebas
        data = {
            "id_usuario": self.usuario.id
        }
        equipo = Equipo.objects.get(id_usuario=data.get('id_usuario'))
        if equipo.jugadores.count()>=25:
            equipo.jugadores.first().delete()

        jugador_extra = Jugador.objects.create(
            nombre="Extra",
            nacionalidad=self.nacionalidad,
            posicion_id=self.pos_del,
        )
        #equipo.jugadores.add(jugador_extra)

        #Segundo asigno un jugador a un equipo:
        url = reverse('add_jugador_equipo', args=[jugador_extra.id])

        response= self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_add_jugador_equipo_invalido(self):
        """Intentamos añadir un jugador a un equipo que no existe"""
        data = {
            "id_usuario": self.usuario.id
        }

        jugador_extra = Jugador.objects.create(
            nombre="Extra",
            nacionalidad=self.nacionalidad,
            posicion_id=self.pos_del,
        )
        # equipo.jugadores.add(jugador_extra)

        # Segundo asigno un jugador a un equipo:
        url = reverse('add_jugador_equipo', args=[jugador_extra.id])

        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_jugador_equipo_valido(self):
        """Comprobamos que podemos eliminar un jugador de un equipo correctamente"""
        # Primero asignamos un equipo

        #Primeor asigno un equipo:
        url_asignar = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        self.client.post(url_asignar, data=data, content_type="application/json")

        #Compruebo que el equipo tenga menos de 25 jugadores si tiene 25 elimino el ultimo para poder hacer las pruebas
        data = {
            "id_usuario": self.usuario.id
        }
        equipo = Equipo.objects.get(id_usuario=data.get('id_usuario'))
        if equipo.jugadores.count()>=25:
            equipo.jugadores.first().delete()

        jugador_extra = Jugador.objects.create(
            nombre="Extra",
            nacionalidad=self.nacionalidad,
            posicion_id=self.pos_del,
        )
        equipo.jugadores.add(jugador_extra)

        url = reverse('delete_jugador_equipo', args=[jugador_extra.id])
        response = self.client.delete(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_jugador_equipo_invalido(self):
        """Intentamos eliminar un jugador de un equipo que en el que no existe"""
        # Primero asignamos un equipo

        # Primeor asigno un equipo:
        url_asignar = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        self.client.post(url_asignar, data=data, content_type="application/json")

        # Compruebo que el equipo tenga menos de 25 jugadores si tiene 25 elimino el ultimo para poder hacer las pruebas
        data = {
            "id_usuario": self.usuario.id
        }

        jugador_extra = Jugador.objects.create(
            nombre="Extra",
            nacionalidad=self.nacionalidad,
            posicion_id=self.pos_del,
        )
        url = reverse('delete_jugador_equipo', args=[jugador_extra.id])
        response = self.client.delete(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

class ExamenTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.rol_usuario = Rol.objects.create(
            nombre='usuario',
        )

        cls.usuario = Usuario.objects.create(
            nombre='vic',
            nick='v',
            correo='v@gmail.com',
            password='12345',
            fecha_nacimiento='1997-09-28'
        )
        rol = Rol.objects.get(nombre="usuario")
        cls.usuario.rol.set([rol])

        cls.pos_por =  Posicion.objects.create(
            siglas = 'POR',
            significado = 'Portero',
            tipo= Posicion.TipoPosicion.PORTERO,
            descripcion = 'La persona que a veces para una pelota entre 3 palos',
        )

        cls.pos_def, _ = Posicion.objects.get_or_create(tipo='DEF', siglas='DEF')
        cls.pos_cen, _ = Posicion.objects.get_or_create(tipo='CEN', siglas='CEN')
        cls.pos_del, _ = Posicion.objects.get_or_create(tipo='DEL', siglas='DEL')


        cls.nacionalidad = Nacionalidad.objects.create(nombre='España')

        for i in range(10):
            Jugador.objects.create(nombre=f'Portero {i}', posicion_id=cls.pos_por, nacionalidad=cls.nacionalidad)
        for i in range(10):
            Jugador.objects.create(nombre=f'Defensa {i}', posicion_id=cls.pos_def, nacionalidad=cls.nacionalidad)
        for i in range(9):
            Jugador.objects.create(nombre=f'Centrocampista {i}', posicion_id=cls.pos_cen, nacionalidad=cls.nacionalidad)
        for i in range(6):
            Jugador.objects.create(nombre=f'Delantero {i}', posicion_id=cls.pos_del, nacionalidad=cls.nacionalidad)


    def test_examen_valido(self):

        #primero asigno un equipo
        url_asignar = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        self.client.post(url_asignar, data=data, content_type="application/json")

        #  url = reverse('get_jugador', args=[999])

        url_calculo= reverse('media_jugador_equipo', args=[self.usuario.id])
        response = self.client.get(url_calculo, content_type="application/json")
        self.assertEqual(response.status_code, 200)


    def test_examen_invalido_menos20Jug(self):
        #primero asigno un equipo
        url_asignar = reverse('asignar_equipo', args=[self.usuario.id])
        data = {"nombre": "Argamasilla", "descripcion": "Equipo con espíritu competitivo"}
        self.client.post(url_asignar, data=data, content_type="application/json")

        #luego quito jugadores
        equipo = Equipo.objects.get(id_usuario=self.usuario.id)
        jugadores_desactivados = 0
        for jugadores in equipo.jugadores.all():
           if f'{jugadores.posicion_id}' != 'Portero'  and jugadores_desactivados < 10:
               jugadores.delete()
               jugadores_desactivados += 1


        url_calculo = reverse('media_jugador_equipo', args=[self.usuario.id])
        response = self.client.get(url_calculo, content_type="application/json")
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_examen_invalido_sin_equipo(self):

        url_calculo = reverse('media_jugador_equipo', args=[self.usuario.id])
        response = self.client.get(url_calculo, content_type="application/json")
        #print(response.content)
        self.assertEqual(response.status_code, 400)